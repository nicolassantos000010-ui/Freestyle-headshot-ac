using System;
using System.Drawing;
using System.Windows.Forms;

namespace FreestyleHeadshot
{
    public class SettingsForm : Form
    {
        private AimbotSettings settings;

        public SettingsForm(AimbotSettings settings)
        {
            this.settings = settings;
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            this.Text = "⚙️  Configurações";
            this.Size = new Size(500, 600);
            this.StartPosition = FormStartPosition.CenterParent;
            this.BackColor = Color.FromArgb(25, 25, 35);
            this.ForeColor = Color.White;
            this.Font = new Font("Segoe UI", 10F);

            var panel = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                RowCount = 12,
                ColumnCount = 2,
                Padding = new Padding(20),
                AutoSize = true
            };

            panel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            panel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));

            var titleLabel = new Label
            {
                Text = "⚙️  CONFIGURAÇÕES DO AIMBOT",
                Font = new Font("Segoe UI", 12F, FontStyle.Bold),
                ForeColor = Color.Cyan,
                AutoSize = true
            };
            panel.Controls.Add(titleLabel, 0, 0);
            panel.SetColumnSpan(titleLabel, 2);

            int row = 1;

            panel.Controls.Add(new Label { Text = "📏 Max Distance:", AutoSize = true }, 0, row);
            var maxDistanceInput = new TextBox { Text = settings.MaxDistance.ToString(), Width = 150 };
            panel.Controls.Add(maxDistanceInput, 1, row);
            row++;

            panel.Controls.Add(new Label { Text = "⚡ Snap Speed:", AutoSize = true }, 0, row);
            var snapSpeedInput = new TextBox { Text = settings.SnapSpeed.ToString(), Width = 150 };
            panel.Controls.Add(snapSpeedInput, 1, row);
            row++;

            panel.Controls.Add(new Label { Text = "🐢 Only on Crouch:", AutoSize = true }, 0, row);
            var crouchCheck = new CheckBox { Checked = settings.OnlyOnCrouch };
            panel.Controls.Add(crouchCheck, 1, row);
            row++;

            panel.Controls.Add(new Label { Text = "👥 Team Check:", AutoSize = true }, 0, row);
            var teamCheck = new CheckBox { Checked = settings.TeamCheck };
            panel.Controls.Add(teamCheck, 1, row);
            row++;

            panel.Controls.Add(new Label { Text = "💀 Dead Check:", AutoSize = true }, 0, row);
            var deadCheck = new CheckBox { Checked = settings.DeadCheck };
            panel.Controls.Add(deadCheck, 1, row);
            row++;

            panel.Controls.Add(new Label { Text = "🧱 Wall Check:", AutoSize = true }, 0, row);
            var wallCheck = new CheckBox { Checked = settings.WallCheck };
            panel.Controls.Add(wallCheck, 1, row);
            row++;

            panel.Controls.Add(new Label { Text = "❤️  Health Check:", AutoSize = true }, 0, row);
            var healthCheck = new CheckBox { Checked = settings.HealthCheck };
            panel.Controls.Add(healthCheck, 1, row);
            row++;

            panel.Controls.Add(new Label { Text = "👁️  FOV:", AutoSize = true }, 0, row);
            var fovInput = new TextBox { Text = settings.FOV.ToString(), Width = 150 };
            panel.Controls.Add(fovInput, 1, row);
            row++;

            row++;

            var saveBtn = new Button
            {
                Text = "💾 Salvar",
                BackColor = Color.FromArgb(0, 120, 215),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Height = 40,
                Width = 200
            };
            saveBtn.Click += (s, e) =>
            {
                try
                {
                    if (float.TryParse(maxDistanceInput.Text, out float maxDist))
                        settings.MaxDistance = maxDist;
                    if (float.TryParse(snapSpeedInput.Text, out float snapSpeed))
                        settings.SnapSpeed = snapSpeed;
                    if (float.TryParse(fovInput.Text, out float fov))
                        settings.FOV = fov;

                    settings.OnlyOnCrouch = crouchCheck.Checked;
                    settings.TeamCheck = teamCheck.Checked;
                    settings.DeadCheck = deadCheck.Checked;
                    settings.WallCheck = wallCheck.Checked;
                    settings.HealthCheck = healthCheck.Checked;

                    MessageBox.Show("✅ Configurações salvas!", "Sucesso", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    this.DialogResult = DialogResult.OK;
                    this.Close();
                }
                catch
                {
                    MessageBox.Show("❌ Erro ao salvar configurações!", "Erro", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            };
            panel.Controls.Add(saveBtn, 0, row);

            var cancelBtn = new Button
            {
                Text = "❌ Cancelar",
                BackColor = Color.FromArgb(150, 150, 150),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Height = 40,
                Width = 200
            };
            cancelBtn.Click += (s, e) => { this.DialogResult = DialogResult.Cancel; this.Close(); };
            panel.Controls.Add(cancelBtn, 1, row);

            var scrollPanel = new Panel { Dock = DockStyle.Fill, AutoScroll = true };
            scrollPanel.Controls.Add(panel);
            this.Controls.Add(scrollPanel);
        }
    }
}
