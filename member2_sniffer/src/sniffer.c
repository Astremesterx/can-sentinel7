#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
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
struct can_stat stats[MAX_CAN_ID] = {0};

double get_current_time() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + (tv.tv_usec / 1000000.0);
}

int main(int argc, char **argv) {
    int s;
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame;
    
    const char *ifname = "vcan0";
    if (argc > 1) {
        ifname = argv[1];
    }

    if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
        perror("Socket");
        return 1;
    }

    strcpy(ifr.ifr_name, ifname);
    ioctl(s, SIOCGIFINDEX, &ifr);

    memset(&addr, 0, sizeof(addr));
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Bind");
        return 1;
    }

    // Print CSV header
    printf("timestamp,sequence_num,can_id,dlc,payload,message_count,frequency,inter_arrival_time\n");
    fflush(stdout);

    unsigned long long global_seq = 0;

    while (1) {
        int nbytes = read(s, &frame, sizeof(struct can_frame));

        if (nbytes < 0) {
            perror("Read");
            return 1;
        }

        if (nbytes < (int)sizeof(struct can_frame)) {
            fprintf(stderr, "Incomplete CAN frame\n");
            continue;
        }

        double current_time = get_current_time();
        
        // Only process standard IDs
        if (frame.can_id & CAN_EFF_FLAG) {
            continue; 
        }
        
        int id = frame.can_id & CAN_ERR_MASK; // Mask off error/rtr flags just in case
        
        if (id >= MAX_CAN_ID) continue; // Out of bounds safety check

        // Calculate features
        stats[id].count++;
        
        double inter_arrival_time = 0.0;
        double frequency = 0.0;
        
        if (stats[id].last_timestamp > 0) {
            inter_arrival_time = current_time - stats[id].last_timestamp;
            if (inter_arrival_time > 0) {
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
        // Handle empty payload case
        if (frame.can_dlc == 0) {
            printf("NULL");
        }
        
        printf(",%llu,%.4f,%.6f\n", stats[id].count, frequency, inter_arrival_time);
        
        // Flush to ensure ML engine gets data immediately via pipe
        fflush(stdout);
    }

    close(s);
    return 0;
}
