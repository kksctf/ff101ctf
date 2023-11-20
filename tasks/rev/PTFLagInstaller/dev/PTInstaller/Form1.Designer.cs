namespace PTInstaller;

partial class FormMain
{
    /// <summary>
    ///  Required designer variable.
    /// </summary>
    private System.ComponentModel.IContainer components = null;

    /// <summary>
    ///  Clean up any resources being used.
    /// </summary>
    /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
    protected override void Dispose(bool disposing)
    {
        if (disposing && (components != null))
        {
            components.Dispose();
        }
        base.Dispose(disposing);
    }

    #region Windows Form Designer generated code

    /// <summary>
    ///  Required method for Designer support - do not modify
    ///  the contents of this method with the code editor.
    /// </summary>
    private void InitializeComponent()
    {
        System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormMain));
        pictureBox_PtLogo = new PictureBox();
        label1 = new Label();
        richTextBox1 = new RichTextBox();
        radioButton_Yes = new RadioButton();
        radioButton_No = new RadioButton();
        button_License_Next = new Button();
        button_Exit = new Button();
        groupBox_License = new GroupBox();
        label2 = new Label();
        groupBox_LicenseKey = new GroupBox();
        label3 = new Label();
        textBox_Lkey_4 = new TextBox();
        textBox_Lkey_3 = new TextBox();
        textBox_Lkey_2 = new TextBox();
        textBox_Lkey_1 = new TextBox();
        groupBox_ChooseRadioGroup = new GroupBox();
        groupBox_InstallProcess = new GroupBox();
        label4 = new Label();
        progressBar_Install = new ProgressBar();
        backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
        ((System.ComponentModel.ISupportInitialize)pictureBox_PtLogo).BeginInit();
        groupBox_License.SuspendLayout();
        groupBox_LicenseKey.SuspendLayout();
        groupBox_ChooseRadioGroup.SuspendLayout();
        groupBox_InstallProcess.SuspendLayout();
        SuspendLayout();
        // 
        // pictureBox_PtLogo
        // 
        pictureBox_PtLogo.BackColor = Color.Red;
        pictureBox_PtLogo.Image = Properties.Resources.ptlogo;
        pictureBox_PtLogo.Location = new Point(2, -2);
        pictureBox_PtLogo.Name = "pictureBox_PtLogo";
        pictureBox_PtLogo.Size = new Size(400, 552);
        pictureBox_PtLogo.SizeMode = PictureBoxSizeMode.Zoom;
        pictureBox_PtLogo.TabIndex = 0;
        pictureBox_PtLogo.TabStop = false;
        // 
        // label1
        // 
        label1.Font = new Font("Segoe UI", 9F, FontStyle.Regular, GraphicsUnit.Point);
        label1.Location = new Point(6, 43);
        label1.Name = "label1";
        label1.Size = new Size(501, 45);
        label1.TabIndex = 1;
        label1.Text = "Пожалуйста, прочтите соглашение ниже и согласитесь. Либо не соглашайтесь, но флага тогда не получите.";
        // 
        // richTextBox1
        // 
        richTextBox1.Location = new Point(6, 102);
        richTextBox1.Name = "richTextBox1";
        richTextBox1.Size = new Size(501, 317);
        richTextBox1.TabIndex = 2;
        richTextBox1.Text = resources.GetString("richTextBox1.Text");
        // 
        // radioButton_Yes
        // 
        radioButton_Yes.AutoSize = true;
        radioButton_Yes.Location = new Point(18, 31);
        radioButton_Yes.Name = "radioButton_Yes";
        radioButton_Yes.Size = new Size(132, 24);
        radioButton_Yes.TabIndex = 3;
        radioButton_Yes.TabStop = true;
        radioButton_Yes.Text = "Да, я согласен.";
        radioButton_Yes.UseVisualStyleBackColor = true;
        // 
        // radioButton_No
        // 
        radioButton_No.AutoSize = true;
        radioButton_No.Location = new Point(18, 61);
        radioButton_No.Name = "radioButton_No";
        radioButton_No.Size = new Size(269, 24);
        radioButton_No.TabIndex = 4;
        radioButton_No.TabStop = true;
        radioButton_No.Text = "Нет, я не буду устанавливать флаг.";
        radioButton_No.UseVisualStyleBackColor = true;
        // 
        // button_License_Next
        // 
        button_License_Next.Location = new Point(744, 439);
        button_License_Next.Name = "button_License_Next";
        button_License_Next.Size = new Size(190, 40);
        button_License_Next.TabIndex = 5;
        button_License_Next.Text = "Далее";
        button_License_Next.UseVisualStyleBackColor = true;
        button_License_Next.Click += button_License_Next_Click;
        // 
        // button_Exit
        // 
        button_Exit.Location = new Point(744, 485);
        button_Exit.Name = "button_Exit";
        button_Exit.Size = new Size(190, 40);
        button_Exit.TabIndex = 6;
        button_Exit.Text = "Отмена";
        button_Exit.UseVisualStyleBackColor = true;
        button_Exit.Click += button_Exit_Click;
        // 
        // groupBox_License
        // 
        groupBox_License.Controls.Add(label2);
        groupBox_License.Controls.Add(label1);
        groupBox_License.Controls.Add(richTextBox1);
        groupBox_License.Location = new Point(419, 0);
        groupBox_License.Name = "groupBox_License";
        groupBox_License.Size = new Size(513, 425);
        groupBox_License.TabIndex = 7;
        groupBox_License.TabStop = false;
        groupBox_License.Visible = false;
        // 
        // label2
        // 
        label2.AutoSize = true;
        label2.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point);
        label2.Location = new Point(6, 23);
        label2.Name = "label2";
        label2.Size = new Size(246, 20);
        label2.TabIndex = 3;
        label2.Text = "ЛИЦЕНЗИОННОЕ СОГЛАШЕНИЕ.";
        // 
        // groupBox_LicenseKey
        // 
        groupBox_LicenseKey.Controls.Add(label3);
        groupBox_LicenseKey.Controls.Add(textBox_Lkey_4);
        groupBox_LicenseKey.Controls.Add(textBox_Lkey_3);
        groupBox_LicenseKey.Controls.Add(textBox_Lkey_2);
        groupBox_LicenseKey.Controls.Add(textBox_Lkey_1);
        groupBox_LicenseKey.Location = new Point(419, 0);
        groupBox_LicenseKey.Name = "groupBox_LicenseKey";
        groupBox_LicenseKey.Size = new Size(513, 425);
        groupBox_LicenseKey.TabIndex = 4;
        groupBox_LicenseKey.TabStop = false;
        groupBox_LicenseKey.Visible = false;
        // 
        // label3
        // 
        label3.AutoSize = true;
        label3.Location = new Point(9, 169);
        label3.Name = "label3";
        label3.Size = new Size(217, 20);
        label3.TabIndex = 4;
        label3.Text = "Введите лицензионный ключ:";
        // 
        // textBox_Lkey_4
        // 
        textBox_Lkey_4.Font = new Font("Consolas", 9F, FontStyle.Regular, GraphicsUnit.Point);
        textBox_Lkey_4.Location = new Point(381, 192);
        textBox_Lkey_4.MaxLength = 8;
        textBox_Lkey_4.Name = "textBox_Lkey_4";
        textBox_Lkey_4.Size = new Size(125, 25);
        textBox_Lkey_4.TabIndex = 3;
        textBox_Lkey_4.TextAlign = HorizontalAlignment.Center;
        // 
        // textBox_Lkey_3
        // 
        textBox_Lkey_3.Font = new Font("Consolas", 9F, FontStyle.Regular, GraphicsUnit.Point);
        textBox_Lkey_3.Location = new Point(257, 192);
        textBox_Lkey_3.MaxLength = 8;
        textBox_Lkey_3.Name = "textBox_Lkey_3";
        textBox_Lkey_3.Size = new Size(125, 25);
        textBox_Lkey_3.TabIndex = 2;
        textBox_Lkey_3.TextAlign = HorizontalAlignment.Center;
        // 
        // textBox_Lkey_2
        // 
        textBox_Lkey_2.Font = new Font("Consolas", 9F, FontStyle.Regular, GraphicsUnit.Point);
        textBox_Lkey_2.Location = new Point(137, 192);
        textBox_Lkey_2.MaxLength = 8;
        textBox_Lkey_2.Name = "textBox_Lkey_2";
        textBox_Lkey_2.Size = new Size(125, 25);
        textBox_Lkey_2.TabIndex = 1;
        textBox_Lkey_2.TextAlign = HorizontalAlignment.Center;
        // 
        // textBox_Lkey_1
        // 
        textBox_Lkey_1.Font = new Font("Consolas", 9F, FontStyle.Regular, GraphicsUnit.Point);
        textBox_Lkey_1.Location = new Point(13, 192);
        textBox_Lkey_1.MaxLength = 8;
        textBox_Lkey_1.Name = "textBox_Lkey_1";
        textBox_Lkey_1.Size = new Size(125, 25);
        textBox_Lkey_1.TabIndex = 0;
        textBox_Lkey_1.TextAlign = HorizontalAlignment.Center;
        // 
        // groupBox_ChooseRadioGroup
        // 
        groupBox_ChooseRadioGroup.Controls.Add(radioButton_Yes);
        groupBox_ChooseRadioGroup.Controls.Add(radioButton_No);
        groupBox_ChooseRadioGroup.Location = new Point(419, 431);
        groupBox_ChooseRadioGroup.Name = "groupBox_ChooseRadioGroup";
        groupBox_ChooseRadioGroup.Size = new Size(319, 94);
        groupBox_ChooseRadioGroup.TabIndex = 8;
        groupBox_ChooseRadioGroup.TabStop = false;
        groupBox_ChooseRadioGroup.Text = "Вы согласны?";
        groupBox_ChooseRadioGroup.Visible = false;
        // 
        // groupBox_InstallProcess
        // 
        groupBox_InstallProcess.Controls.Add(label4);
        groupBox_InstallProcess.Controls.Add(progressBar_Install);
        groupBox_InstallProcess.Location = new Point(419, 0);
        groupBox_InstallProcess.Name = "groupBox_InstallProcess";
        groupBox_InstallProcess.Size = new Size(513, 425);
        groupBox_InstallProcess.TabIndex = 9;
        groupBox_InstallProcess.TabStop = false;
        groupBox_InstallProcess.Visible = false;
        // 
        // label4
        // 
        label4.AutoSize = true;
        label4.Location = new Point(10, 141);
        label4.Name = "label4";
        label4.Size = new Size(343, 20);
        label4.TabIndex = 1;
        label4.Text = "Идет установка флага. Пожалуйста, подождите...";
        // 
        // progressBar_Install
        // 
        progressBar_Install.Location = new Point(13, 164);
        progressBar_Install.Maximum = 200;
        progressBar_Install.Name = "progressBar_Install";
        progressBar_Install.Size = new Size(493, 29);
        progressBar_Install.TabIndex = 0;
        // 
        // backgroundWorker1
        // 
        backgroundWorker1.WorkerReportsProgress = true;
        backgroundWorker1.WorkerSupportsCancellation = true;
        backgroundWorker1.DoWork += backgroundWorker1_DoWork;
        backgroundWorker1.ProgressChanged += backgroundWorker1_ProgressChanged;
        backgroundWorker1.RunWorkerCompleted += backgroundWorker1_RunWorkerCompleted;
        // 
        // FormMain
        // 
        AutoScaleDimensions = new SizeF(8F, 20F);
        AutoScaleMode = AutoScaleMode.Font;
        BackColor = SystemColors.ButtonFace;
        ClientSize = new Size(944, 553);
        Controls.Add(groupBox_InstallProcess);
        Controls.Add(groupBox_LicenseKey);
        Controls.Add(groupBox_ChooseRadioGroup);
        Controls.Add(groupBox_License);
        Controls.Add(button_Exit);
        Controls.Add(button_License_Next);
        Controls.Add(pictureBox_PtLogo);
        FormBorderStyle = FormBorderStyle.FixedSingle;
        Icon = (Icon)resources.GetObject("$this.Icon");
        ImeMode = ImeMode.On;
        MaximizeBox = false;
        MinimizeBox = false;
        Name = "FormMain";
        ShowInTaskbar = false;
        Text = "PT Flag Installer";
        TopMost = true;
        ((System.ComponentModel.ISupportInitialize)pictureBox_PtLogo).EndInit();
        groupBox_License.ResumeLayout(false);
        groupBox_License.PerformLayout();
        groupBox_LicenseKey.ResumeLayout(false);
        groupBox_LicenseKey.PerformLayout();
        groupBox_ChooseRadioGroup.ResumeLayout(false);
        groupBox_ChooseRadioGroup.PerformLayout();
        groupBox_InstallProcess.ResumeLayout(false);
        groupBox_InstallProcess.PerformLayout();
        ResumeLayout(false);
    }

    #endregion

    private PictureBox pictureBox_PtLogo;
    private Label label1;
    private RichTextBox richTextBox1;
    private RadioButton radioButton_Yes;
    private RadioButton radioButton_No;
    private Button button_License_Next;
    private Button button_Exit;
    private GroupBox groupBox_License;
    private GroupBox groupBox_ChooseRadioGroup;
    private Label label2;
    private GroupBox groupBox_LicenseKey;
    private TextBox textBox_Lkey_4;
    private TextBox textBox_Lkey_3;
    private TextBox textBox_Lkey_2;
    private TextBox textBox_Lkey_1;
    private Label label3;
    private GroupBox groupBox_InstallProcess;
    private Label label4;
    private ProgressBar progressBar_Install;
    private System.ComponentModel.BackgroundWorker backgroundWorker1;
}