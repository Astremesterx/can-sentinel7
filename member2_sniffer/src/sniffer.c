#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <linux/can.h>
#include <linux/can/raw.h>

#define MAX_CAN_ID 0x800

struct can_stat {
    unsigned long long count;
    double last_timestamp;
};

// Track statistics for standard CAN IDs (0x000 to 0x7FF)
static struct can_stat stats[MAX_CAN_ID] = {0};
static volatile sig_atomic_t keep_running = 1;

static void handle_signal(int sig) {
    (void)sig;
    keep_running = 0;
}

static double get_current_time(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + (tv.tv_usec / 1000000.0);
}

int main(int argc, char **argv) {
    int s;
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame;

    // Register clean signal handlers
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = handle_signal;
    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);
    signal(SIGPIPE, SIG_IGN); // Prevent abrupt crash if downstream pipe closes

    const char *ifname = "vcan0";
    if (argc > 1) {
        ifname = argv[1];
    }

    if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
        perror("Socket");
        return 1;
    }

    strncpy(ifr.ifr_name, ifname, IFNAMSIZ - 1);
    ifr.ifr_name[IFNAMSIZ - 1] = '\0';
    if (ioctl(s, SIOCGIFINDEX, &ifr) < 0) {
        perror("SIOCGIFINDEX");
        close(s);
        return 1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Bind");
        close(s);
        return 1;
    }

    // Print CSV header
    printf("timestamp,sequence_num,can_id,dlc,payload,message_count,frequency,inter_arrival_time\n");
    fflush(stdout);

    unsigned long long global_seq = 0;
    double start_time = get_current_time();

    while (keep_running) {
        int nbytes = read(s, &frame, sizeof(struct can_frame));

        if (nbytes < 0) {
            if (!keep_running) break;
            perror("Read");
            break;
        }

        if (nbytes < (int)sizeof(struct can_frame)) {
            fprintf(stderr, "Incomplete CAN frame received\n");
            continue;
        }

        double current_time = get_current_time();

        // Only process standard 11-bit CAN frames (skip extended / error / RTR frames)
        if (frame.can_id & (CAN_EFF_FLAG | CAN_ERR_FLAG | CAN_RTR_FLAG)) {
            continue;
        }

        int id = frame.can_id & CAN_SFF_MASK;

        if (id >= MAX_CAN_ID) continue;

        // Calculate features
        stats[id].count++;

        double inter_arrival_time = 0.0;
        double frequency = 0.0;

        if (stats[id].last_timestamp > 0.0) {
            inter_arrival_time = current_time - stats[id].last_timestamp;
            if (inter_arrival_time > 0.0) {
                frequency = 1.0 / inter_arrival_time;
            }
        }

        stats[id].last_timestamp = current_time;
        global_seq++;

        // Print features
        printf("%.6f,%llu,%03X,%d,", current_time, global_seq, id, frame.can_dlc);

        // Print payload in hex
        for (int i = 0; i < frame.can_dlc; i++) {
            printf("%02X", frame.data[i]);
        }
        if (frame.can_dlc == 0) {
            printf("NULL");
        }

        printf(",%llu,%.4f,%.6f\n", stats[id].count, frequency, inter_arrival_time);
        fflush(stdout);
    }

    close(s);

    // Print summary telemetry to stderr upon clean exit
    double elapsed = get_current_time() - start_time;
    int active_ids = 0;
    for (int i = 0; i < MAX_CAN_ID; i++) {
        if (stats[i].count > 0) active_ids++;
    }

    fprintf(stderr, "\n[+] CAN-Sentinel Sniffer closed cleanly.\n");
    fprintf(stderr, "    Total frames processed : %llu\n", global_seq);
    fprintf(stderr, "    Active CAN IDs tracked : %d\n", active_ids);
    if (elapsed > 0.0) {
        fprintf(stderr, "    Capture duration       : %.2f sec (%.1f frames/sec)\n", elapsed, (double)global_seq / elapsed);
    }

    return 0;
}
