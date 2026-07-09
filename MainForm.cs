using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Windows.Forms;
using System.Linq;

namespace FreestyleHeadshot
{
    public partial class MainForm : Form
    {
        private AimbotManager aimbotManager;
        private bool isRunning = false;

        public MainForm()
        {
            InitializeComponent();
            aimbotManager = new AimbotManager();
            this.Text = "🎮 Freestyle Headshot AC v1.0";
            this.FormClosing += MainForm_FormClosing;
        }

        private void InitializeComponent()
        {
            this.SuspendLayout();

            this.AutoScaleDimensions = new SizeF(7F, 15F);
            this.AutoScaleMode = AutoScaleMode.Font;
            this.ClientSize = new Size(700, 700);
            this.Font = new Font("Segoe UI", 10F);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.FromArgb(25, 25, 35);
            this.ForeColor = Color.White;

            var mainPanel = new Panel
            {
                Dock = DockStyle.Fill,
                AutoScroll = true,
                BackColor = Color.FromArgb(25, 25, 35)
            };

            var titleLabel = new Label
            {
                Text = "FREESTYLE HEADSHOT AC\nMENU PRINCIPAL",
                Font = new Font("Courier New", 12F, FontStyle.Bold),
                ForeColor = Color.Cyan,
                Dock = DockStyle.Top,
                Height = 80,
                TextAlign = ContentAlignment.TopCenter,
                Padding = new Padding(10)
            };
            mainPanel.Controls.Add(titleLabel);

            var statusPanel = new Panel
            {
                Dock = DockStyle.Top,
                Height = 50,
                BackColor = Color.FromArgb(35, 35, 50),
                BorderStyle = BorderStyle.FixedSingle
            };
            var statusLabel = new Label
            {
                Text = "Status: ❌ DESATIVADO",
                Font = new Font("Segoe UI", 12F, FontStyle.Bold),
                ForeColor = Color.Red,
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleCenter,
                Name = "statusLabel"
            };
            statusPanel.Controls.Add(statusLabel);
            mainPanel.Controls.Add(statusPanel);

            var buttonsPanel = new FlowLayoutPanel
            {
                Dock = DockStyle.Top,
                Height = 300,
                AutoSize = false,
                FlowDirection = FlowDirection.TopDown,
                Padding = new Padding(10),
                BackColor = Color.FromArgb(25, 25, 35)
            };

            var startBtn = new Button
            {
                Text = "▶️  Iniciar Aimbot",
                Size = new Size(300, 50),
                Font = new Font("Segoe UI", 11F, FontStyle.Bold),
                BackColor = Color.FromArgb(0, 120, 215),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Margin = new Padding(5)
            };
            startBtn.Click += StartBtn_Click;
            buttonsPanel.Controls.Add(startBtn);

            var stopBtn = new Button
            {
                Text = "⏹️  Parar Aimbot",
                Size = new Size(300, 50),
                Font = new Font("Segoe UI", 11F, FontStyle.Bold),
                BackColor = Color.FromArgb(200, 0, 0),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Margin = new Padding(5),
                Enabled = false,
                Name = "stopBtn"
            };
            stopBtn.Click += StopBtn_Click;
            buttonsPanel.Controls.Add(stopBtn);

            var settingsBtn = new Button
            {
                Text = "⚙️  Configurações",
                Size = new Size(300, 50),
                Font = new Font("Segoe UI", 11F, FontStyle.Bold),
                BackColor = Color.FromArgb(100, 100, 100),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Margin = new Padding(5)
            };
            settingsBtn.Click += SettingsBtn_Click;
            buttonsPanel.Controls.Add(settingsBtn);

            var scannerBtn = new Button
            {
                Text = "🔍 Scanner de Offsets",
                Size = new Size(300, 50),
                Font = new Font("Segoe UI", 11F, FontStyle.Bold),
                BackColor = Color.FromArgb(100, 100, 100),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Margin = new Padding(5)
            };
            scannerBtn.Click += ScannerBtn_Click;
            buttonsPanel.Controls.Add(scannerBtn);

            mainPanel.Controls.Add(buttonsPanel);

            var logLabel = new Label
            {
                Text = "📋 LOG DE EVENTOS:",
                Font = new Font("Segoe UI", 10F, FontStyle.Bold),
                ForeColor = Color.Yellow,
                Height = 30,
                Dock = DockStyle.Top
            };
            mainPanel.Controls.Add(logLabel);

            var logTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Vertical,
                BackColor = Color.FromArgb(35, 35, 50),
                ForeColor = Color.Lime,
                Font = new Font("Courier New", 9F),
                Name = "logTextBox"
            };
            mainPanel.Controls.Add(logTextBox);

            this.Controls.Add(mainPanel);
            this.ResumeLayout(false);
        }

        private void StartBtn_Click(object sender, EventArgs e)
        {
            var statusLabel = this.Controls[0].Controls.OfType<Panel>().FirstOrDefault()?.Controls[0] as Label;
            var stopBtn = this.Controls[0].Controls.OfType<Button>().FirstOrDefault(b => b.Name == "stopBtn");
            var startBtn = sender as Button;

            if (!isRunning)
            {
                var logBox = this.Controls[0].Controls.OfType<TextBox>().FirstOrDefault();
                logBox?.AppendText("[INFO] Procurando AssaultCube...\r\n");

                if (aimbotManager.FindAndAttachToGame())
                {
                    isRunning = true;
                    aimbotManager.StartAimbot();
                    
                    if (statusLabel != null)
                    {
                        statusLabel.Text = "Status: ✅ ATIVADO";
                        statusLabel.ForeColor = Color.Lime;
                    }
                    if (stopBtn != null) stopBtn.Enabled = true;
                    if (startBtn != null) startBtn.Enabled = false;
                    
                    logBox?.AppendText("[SUCCESS] Aimbot iniciado!\r\n");
                }
                else
                {
                    logBox?.AppendText("[ERROR] AssaultCube não encontrado!\r\n");
                    MessageBox.Show("AssaultCube não foi encontrado.\nCertifique-se de que o jogo está aberto.", "Erro", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void StopBtn_Click(object sender, EventArgs e)
        {
            var statusLabel = this.Controls[0].Controls.OfType<Panel>().FirstOrDefault()?.Controls[0] as Label;
            var stopBtn = sender as Button;
            var startBtn = this.Controls[0].Controls.OfType<Button>().FirstOrDefault();

            if (isRunning)
            {
                isRunning = false;
                aimbotManager.StopAimbot();
                
                if (statusLabel != null)
                {
                    statusLabel.Text = "Status: ❌ DESATIVADO";
                    statusLabel.ForeColor = Color.Red;
                }
                if (stopBtn != null) stopBtn.Enabled = false;
                if (startBtn != null) startBtn.Enabled = true;
                
                var logBox = this.Controls[0].Controls.OfType<TextBox>().FirstOrDefault();
                logBox?.AppendText("[STOP] Aimbot desativado!\r\n");
            }
        }

        private void SettingsBtn_Click(object sender, EventArgs e)
        {
            var settingsForm = new SettingsForm(aimbotManager.Settings);
            settingsForm.ShowDialog(this);
        }

        private void ScannerBtn_Click(object sender, EventArgs e)
        {
            var scannerForm = new ScannerForm();
            scannerForm.ShowDialog(this);
        }

        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (isRunning)
            {
                aimbotManager.StopAimbot();
            }
        }
    }
}
