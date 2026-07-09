using System;
using System.Windows.Forms;

namespace FreestyleHeadshot
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            ApplicationConfiguration.Initialize();
            Application.Run(new MainForm());
        }
    }
}
