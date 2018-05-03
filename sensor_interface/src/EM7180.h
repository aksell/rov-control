#ifndef EM7180_H
#define EM7180_h

#include <math.h> /* sqrt */
#include <stdint.h>

#include "ros/ros.h"
//#include <dynamic_reconfigure/server.h>
#include "sensor_msgs"

class EM7180 {
public:
  static void setPassThrough();

private:
  uint8_t i2cAddress 0x28;
  bool passThrough false;

  // EM7180 SEntral registers, see
  // http://www.emdeveloper.com/downloads/7180/EMSentral_EM7180_Register_Map_v1_3.pdf
  const uint8_t EM7180_QX 0x00;
  const uint8_t EM7180_QY 0x04;
  const uint8_t EM7180_QZ 0x08;
  const uint8_t EM7180_QW 0x0C;
  const uint8_t EM7180_QTIME 0x10;

  const uint8_t EM7180_MX 0x12;
  const uint8_t EM7180_MY 0x14;
  const uint8_t EM7180_MZ 0x16;
  const uint8_t EM7180_MTIME 0x18;
  const uint8_t EM7180_AX 0x1A;
  const uint8_t EM7180_AY 0x1C;
  const uint8_t EM7180_AZ 0x1E;
  const uint8_t EM7180_ATIME 0x20;
  const uint8_t EM7180_GX 0x22;
  const uint8_t EM7180_GY 0x24;
  const uint8_t EM7180_GZ 0x26;
  const uint8_t EM7180_GTIME 0x28;
  const uint8_t EM7180_Baro 0x2A;

  const uint8_t EM7180_BaroTIME 0x2C;
  const uint8_t EM7180_Temp 0x2E;
  const uint8_t EM7180_TempTIME 0x30;

  const uint8_t EM7180_QRateDivisor 0x32;
  const uint8_t EM7180_EnableEvents 0x33;
  const uint8_t EM7180_HostControl 0x34;
  const uint8_t EM7180_EventStatus 0x35;
  const uint8_t EM7180_SensorStatus 0x36;
  const uint8_t EM7180_SentralStatus 0x37;
  const uint8_t EM7180_AlgorithmStatus 0x38;
  const uint8_t EM7180_FeatureFlags 0x39;
  const uint8_t EM7180_ParamAcknowledge 0x3A;
  const uint8_t EM7180_SavedParamByte0 0x3B;
  const uint8_t EM7180_SavedParamByte1 0x3C;
  const uint8_t EM7180_SavedParamByte2 0x3D;
  const uint8_t EM7180_SavedParamByte3 0x3E;
  const uint8_t EM7180_ActualMagRate 0x45;
  const uint8_t EM7180_ActualAccelRate 0x46;
  const uint8_t EM7180_ActualGyroRate 0x47;
  const uint8_t EM7180_ActualBaroRate 0x48;
  const uint8_t EM7180_ActualTempRate 0x49;
  const uint8_t EM7180_ErrorRegister 0x50;
  const uint8_t EM7180_AlgorithmControl 0x54;
  const uint8_t EM7180_MagRate 0x55;
  const uint8_t EM7180_AccelRate 0x56;
  const uint8_t EM7180_GyroRate 0x57;

  const uint8_t EM7180_BaroRate 0x58;
  const uint8_t EM7180_TempRate 0x59;
  const uint8_t EM7180_LoadParamByte0 0x60;
  const uint8_t EM7180_LoadParamByte1 0x61;
  const uint8_t EM7180_LoadParamByte2 0x62;
  const uint8_t EM7180_LoadParamByte3 0x63;
  const uint8_t EM7180_ParamRequest 0x64;

  const uint8_t EM7180_ROMVersion1 0x70;
  const uint8_t EM7180_ROMVersion2 0x71;
  const uint8_t EM7180_RAMVersion1 0x72;
  const uint8_t EM7180_RAMVersion2 0x73;
  const uint8_t EM7180_ProductID 0x90;
  const uint8_t EM7180_RevisionID 0x91;
  const uint8_t EM7180_RunStatus 0x92;
  const uint8_t EM7180_UploadAddress 0x94;
  const uint8_t EM7180_UploadData 0x96;
  const uint8_t EM7180_CRCHost 0x97;
  const uint8_t EM7180_PassThruStatus 0x9E;
  const uint8_t EM7180_PassThruControl 0xA0;
  const uint8_t EM7180_ACC_LPF_BW 0x5B;
  const uint8_t EM7180_GYRO_LPF_BW 0x5C;
  const uint8_t EM7180_BARO_LPF_BW 0x5D;
}

#endif
