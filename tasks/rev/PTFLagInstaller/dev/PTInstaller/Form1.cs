using System.Security.Cryptography;

namespace PTInstaller
{
    public partial class FormMain : Form
    {
        bool stage_license;
        bool stage_key;
        bool stage_install;
        bool stage_comlete;

        LicenseKeyCheck? checker;
        StreamWriter? flagfile;

        bool stage1 = true;
        bool stage2 = true;
        bool stage3 = true;
        bool stage4 = true;

        public FormMain()
        {
            InitializeComponent();

            stage_license = true;
            stage_key = false;
            stage_install = false;
            stage_comlete = false;

            groupBox_License.Visible = true;
            groupBox_ChooseRadioGroup.Visible = true;
            groupBox_LicenseKey.Visible = false;
        }

        private void button_License_Next_Click(object sender, EventArgs e)
        {
            if (stage_license)
            {
                if (radioButton_Yes.Checked)
                {
                    groupBox_License.Visible = false;
                    groupBox_ChooseRadioGroup.Visible = false;
                    groupBox_LicenseKey.Visible = true;
                    groupBox_InstallProcess.Visible = false;

                    button_License_Next.Text = "Проверить";

                    stage_key = true;
                    stage_license = false;
                }

                if (radioButton_No.Checked)
                {
                    button_Exit_Click(sender, e);
                }

                return;
            }
            if (stage_key)
            {
                // TODO
                /*  Положение формочек:
                    3 2 4 1
                       V
                    1 2 3 4
                */
                string data_part1 = textBox_Lkey_3.Text.Trim();
                string data_part2 = textBox_Lkey_2.Text.Trim();
                string data_part3 = textBox_Lkey_4.Text.Trim();
                string data_part4 = textBox_Lkey_1.Text.Trim();

                checker = new(data_part1, data_part2, data_part3, data_part4);

                if (checker.result == 4)
                {
                    groupBox_LicenseKey.Visible = false;
                    groupBox_InstallProcess.Visible = true;

                    stage_key = false;
                    stage_install = true;

                    button_License_Next.Text = "Установка...";
                    button_License_Next.Enabled = false;

                    string home_folder = System.Environment.GetFolderPath(System.Environment.SpecialFolder.Personal);
                    flagfile = File.CreateText(home_folder + "\\flag.txt");

                    if (!backgroundWorker1.IsBusy)
                    {
                        backgroundWorker1.RunWorkerAsync();
                    }
                }
                else
                {
                    MessageBox.Show("Неправильный лицензионный ключ. \nВаше местоположение определено по IP.\nК вам вызван отряд ФСБ за попытку взлома.",
                        "Ошибка!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }

                return;
            }
            if (stage_install)
            {
                progressBar_Install.Value += 5;
                return;
            }
            if (stage_comlete)
            {
                System.Windows.Forms.Application.Exit();
                return;
            }
        }

        private void button_Exit_Click(object sender, EventArgs e)
        {
            DialogResult result = MessageBox.Show("Вы уверены, что не хотите получить флаг?",
                "Выход",
                MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (result == DialogResult.Yes)
            {
                System.Windows.Forms.Application.Exit();
            }
        }

        private void backgroundWorker1_RunWorkerCompleted(object sender, System.ComponentModel.RunWorkerCompletedEventArgs e)
        {
            stage_install = false;
            stage_comlete = true;
            label4.Text = "Готово!";  // не делайте как я - именуйте все элементы правильно...
            button_Exit.Visible = false;
            button_License_Next.Text = "Выход";
            button_License_Next.Enabled = true;
            flagfile?.Close();
        }

        private void backgroundWorker1_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            int local_val = 0;
            Random rnd_val = new Random();
            Random rnd_time = new Random();

            while (local_val < progressBar_Install.Maximum)
            {

                local_val += rnd_val.Next(5, 20);
                backgroundWorker1.ReportProgress(local_val);
                System.Threading.Thread.Sleep(rnd_time.Next(500, 1500));
            }

            backgroundWorker1.ReportProgress(progressBar_Install.Maximum);
            System.Threading.Thread.Sleep(2000);
            backgroundWorker1.CancelAsync();
        }

        private void backgroundWorker1_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            if (e.ProgressPercentage <= progressBar_Install.Maximum)
            {
                progressBar_Install.Value = e.ProgressPercentage;
            }

            if (checker != null && flagfile != null)
            {
                if (stage1 && progressBar_Install.Value >= 50 && progressBar_Install.Value <= 75)
                {
                    flagfile.Write(checker.GenerateLicenseData_VendorData());
                    stage1 = false;
                }
                if (stage2 && progressBar_Install.Value >= 76 && progressBar_Install.Value <= 100)
                {
                    flagfile.Write(checker.GenerateLicenseData_CodeData());
                    stage2 = false;
                }
                if (stage3 && progressBar_Install.Value >= 125 && progressBar_Install.Value <= 150)
                {
                    flagfile.Write(checker.GenerateLicenseData_EncryptedPart());
                    stage3 = false;
                }
                if (stage4 && progressBar_Install.Value >= 170 && progressBar_Install.Value <= progressBar_Install.Maximum)
                {
                    flagfile.Write(checker.GenerateLicenseData_TimeStamp());
                    stage4 = false;
                }
            }
        }
    }
}