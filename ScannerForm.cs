using System;
using System.Drawing;
using System.Windows.Forms;
using System.Diagnostics;

namespace FreestyleHeadshot
{
    public class ScannerForm : Form
    {
        public ScannerForm()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            this.Text = "🔍 Scanner de Offsets";
            this.Size = new Size(600, 500);
            this.StartPosition = FormStartPosition.CenterParent;
            this.BackColor = Color.FromArgb(25, 25, 35);
            this.ForeColor = Color.White;
            this.Font = new Font("Segoe UI", 10F);

            var panel = new Panel { Dock = DockStyle.Fill, Padding = new Padding(20), AutoScroll = true };

            var titleLabel = new Label
            {
                Text = "🔍 SCANNER DE OFFSETS",
                Font = new Font("Segoe UI", 12F, FontStyle.Bold),
                ForeColor = Color.Cyan,
                Height = 40,
                Dock = DockStyle.Top
            };
            panel.Controls.Add(titleLabel);

            var infoLabel = new Label
            {
                Text = "Este scanner ajuda a encontrar offsets de memória do AssaultCube.\n\n" +
                       "📋 OFFSETS CONHECIDOS:\n" +
                       "• PLAYERS_PTR: 0x0010F4F4\n" +
                       "• POS_X: 0x0\n" +
                       "• POS_Y: 0x4\n" +
                       "• POS_Z: 0x8\n" +
                       "• HEAD_HEIGHT: 1.7\n" +
                       "• HEALTH: 0xF8\n" +
                       "• ARMOR: 0xFC\n" +
                       "• CROUCHING: 0x21C\n" +
                       "• TEAM: 0x30\n" +
                       "• ALIVE: 0x68\n" +
                       "• CAMERA_YAW: 0x40\n" +
                       "• CAMERA_PITCH: 0x44\n" +
                       "• FOV: 0x50\n\n" +
                       "💡 PARA ENCONTRAR NOVOS OFFSETS:\n" +
                       "1. Use Cheat Engine\n" +
                       "2. Acesse fóruns como UnknownCheats\n" +
                       "3. Consulte a wiki da comunidade AssaultCube",
                Font = new Font("Courier New", 9F),
                Height = 350,
                Dock = DockStyle.Top,
                AutoSize = true
            };
            panel.Controls.Add(infoLabel);

            var closeBtn = new Button
            {
                Text = "❌ Fechar",
                BackColor = Color.FromArgb(100, 100, 100),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Height = 40,
                Width = 200,
                Dock = DockStyle.Bottom,
                Margin = new Padding(0, 10, 0, 0)
            };
            closeBtn.Click += (s, e) => this.Close();
            panel.Controls.Add(closeBtn);

            this.Controls.Add(panel);
        }
    }
}
