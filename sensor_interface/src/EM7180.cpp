#include "EM7180.h"

static void setupPassThrough(){
    int fd = wiringPiI2CSetup(EM7180_ADDRESS);

    // First put SENtral in standby mode
    uint8_t c = wiringPiI2CReadReg8(fd, EM7180_AlgorithmControl);
    wiringPiI2CWriteReg8(fd, EM7180_AlgorithmControl, c | 0x01);
    // Verify standby status
    if(wiringPiI2CReadReg8(fd, EM7180_AlgorithmStatus) & 0x01) {
        printf("SENtral in standby mode");
    }
    // Place SENtral in pass-through mode
    wiringPiI2CWriteReg8(fd, EM7180_PassThruControl, 0x01);
    if(wiringPiI2CReadReg8(fd, EM7180_PassThruStatus) & 0x01) {
        printf("SENtral in pass-through mode");
    }
    else {
        printf("ERROR! SENtral not in pass-through mode!");
    }
}
