using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;

namespace PTInstaller
{
    internal class StaticStorage
    {
        public static byte[] data_part_1 = { 0x7b, 0x66, 0x74, 0x63, 0x74, 0x70 };
        public static byte[] data_part_2 = { 0x44, 0x26, 0x1f, 0x41, 0x6c, 0x79, 0x43, 0x4e, 0x07, 0x79, 0x2c };
        public static byte[] data_part_3 = { 0x63, 0x68, 0x20, 0x54, 0x6b, 0x5f, 0x22, 0x44, 0x5f };
        public static byte[] data_part_4 = { 0xfa, 0x42, 0x30, 0x6d, 0xa9, 0x12, 0x67, 0x06, 0xe5 };

        public static byte[] k = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01 };
        public static byte[] iv = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
        public static byte[] enc = { 0x5a, 0xf1, 0xcf, 0x02, 0x68, 0x3d, 0x2d, 0x62, 0x6d, 0xb2, 0x2f, 0x9c, 0x8d, 0x90, 0xb5, 0x85 };
    }
    internal class LicenseKeyCheck
    {

        private uint DataPart1;
        private uint DataPart2;
        private uint DataPart3;
        private uint DataPart4;
        public uint result;

        public LicenseKeyCheck(string dataPart1, string dataPart2, string dataPart3, string dataPart4)
        {
            try
            {
                DataPart1 = uint.Parse(dataPart1, System.Globalization.NumberStyles.HexNumber);
                DataPart2 = uint.Parse(dataPart2, System.Globalization.NumberStyles.HexNumber);
                DataPart3 = uint.Parse(dataPart3, System.Globalization.NumberStyles.HexNumber);
                DataPart4 = uint.Parse(dataPart4, System.Globalization.NumberStyles.HexNumber);

                check();
            }
            catch (FormatException)
            {
                result = 0;
            }
        }

        private void check()
        {
            result = check1() + check2() + check3() + check4();
        }
        private uint check1() 
        {
            // 561affb1
            if (((DataPart1 & 4278190080) >> 0x18) * ((DataPart1 & 16711680) >> 0x10) * ((DataPart1 & 65280) >> 8) * (DataPart1 & 255) == 0x603f204)
            {
                return 1;
            }
            return 0;
        }
        private uint check2() 
        {
            if ((DataPart2 ^ 0xdeadf00d) == 0xEDB88320) { return 1; } // 3315732d
            return 0;
        }
        private uint check3() 
        {
            byte[] encrypted;

            using (Aes aesAlg = Aes.Create())
            {
                aesAlg.Key = StaticStorage.k;
                aesAlg.IV = StaticStorage.iv;
                ICryptoTransform encryptor = aesAlg.CreateEncryptor(aesAlg.Key, aesAlg.IV);
                using (MemoryStream msEncrypt = new MemoryStream())
                {
                    using (CryptoStream csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write))
                    {
                        using (StreamWriter swEncrypt = new StreamWriter(csEncrypt))
                        {
                            swEncrypt.Write(DataPart3 & 0x0000FFFF);
                        }
                        encrypted = msEncrypt.ToArray();
                    }
                }
            }

            if (encrypted.SequenceEqual(StaticStorage.enc))
            {
                DataPart3 = DataPart3 & 0x0000FFFF;
                return 1; 
            
            }
            return 0;
        }
        private uint check4() 
        {
            // TODO: положить в лицензионное соглашение? :D
            DateTime startdate = new DateTime(2077, 10, 11, 0, 0, 0);
            DateTime dateTime = new DateTime(1970, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc);
            dateTime = dateTime.AddSeconds(DataPart4);
            int diff = DateTime.Compare(dateTime, startdate);
            if ( diff > 0)
            {
                return 1;
            }
            return 0;
        }


        // ptctf{ w3ll_l0c4l_ ch3ck_1s_ b4d_1d34}
        // cac3422f 3315732d 561affb1 6d731337  | key
        // 561affb1 3315732d 6d731337 cac3422f  | check order

        public string GenerateLicenseData_VendorData()
        {
            // write "ptctf{"
            Array.Reverse(StaticStorage.data_part_1, 0, StaticStorage.data_part_1.Length);
            return Encoding.UTF8.GetString(StaticStorage.data_part_1);
        }
        public string GenerateLicenseData_CodeData()
        {   
            // write part1_
            byte[] key = BitConverter.GetBytes(DataPart2);
            Array.Reverse(key, 0, key.Length);
            for (int i = 0; i < StaticStorage.data_part_2.Length; i++)
            {
                StaticStorage.data_part_2[i] = (byte)(StaticStorage.data_part_2[i] ^ key[i % 4]);
            }
            return Encoding.UTF8.GetString(StaticStorage.data_part_2);
        }
        public string GenerateLicenseData_EncryptedPart()
        {
            // write part2_
            byte[] key = BitConverter.GetBytes(DataPart3);
            Array.Reverse(key, 0, key.Length);
            for (int i = 0; i < StaticStorage.data_part_3.Length; i++)
            {
                StaticStorage.data_part_3[i] = (byte)(StaticStorage.data_part_3[i] ^ key[i % 4]);
            }
            return Encoding.UTF8.GetString(StaticStorage.data_part_3);
        }
        public string GenerateLicenseData_TimeStamp()
        {
            // write part3}
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormMain));
            string license = resources.GetString("richTextBox1.Text");
            int key_str_pos = license.IndexOf("12345678-abcdef00-00fedcba-");
            string key_str = license.Substring(key_str_pos+27, 8);
            byte[] key = BitConverter.GetBytes(uint.Parse(key_str, System.Globalization.NumberStyles.HexNumber));
            Array.Reverse(key, 0, key.Length);
            for (int i = 0; i < StaticStorage.data_part_4.Length; i++)
            {
                StaticStorage.data_part_4[i] = (byte)(StaticStorage.data_part_4[i] ^ key[i % 4]);
            }
            return Encoding.UTF8.GetString(StaticStorage.data_part_4);
        }
    }
}
