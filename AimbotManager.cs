using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
using System.Threading.Tasks;

namespace FreestyleHeadshot
{
    public class Vector3
    {
        public float X, Y, Z;

        public Vector3(float x = 0, float y = 0, float z = 0)
        {
            X = x;
            Y = y;
            Z = z;
        }

        public float DistanceTo(Vector3 other)
        {
            float dx = other.X - X;
            float dy = other.Y - Y;
            float dz = other.Z - Z;
            return (float)Math.Sqrt(dx * dx + dy * dy + dz * dz);
        }

        public override string ToString() => $"Vector3({X:F2}, {Y:F2}, {Z:F2})";
    }

    public class PlayerInfo
    {
        public Vector3 Position { get; set; } = new Vector3();
        public Vector3 HeadPosition { get; set; } = new Vector3();
        public int Health { get; set; }
        public int Armor { get; set; }
        public bool IsCrouching { get; set; }
        public int Team { get; set; }
        public bool IsAlive { get; set; }
        public int Index { get; set; }
    }

    public class AimbotSettings
    {
        public float MaxDistance { get; set; } = 100;
        public float SnapSpeed { get; set; } = 0.8f;
        public bool OnlyOnCrouch { get; set; } = true;
        public bool TeamCheck { get; set; } = true;
        public bool DeadCheck { get; set; } = true;
        public bool WallCheck { get; set; } = true;
        public bool HealthCheck { get; set; } = true;
        public float FOV { get; set; } = 180;
        public bool Enabled { get; set; } = false;
    }

    public class AimbotManager
    {
        [DllImport("kernel32.dll")]
        private static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInheritHandle, uint dwProcessId);

        [DllImport("kernel32.dll")]
        private static extern bool ReadProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, uint nSize, out uint lpNumberOfBytesRead);

        [DllImport("kernel32.dll")]
        private static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, uint nSize, out uint lpNumberOfBytesWritten);

        [DllImport("kernel32.dll")]
        private static extern bool CloseHandle(IntPtr hObject);

        private const uint PROCESS_VM_READ = 0x0010;
        private const uint PROCESS_VM_WRITE = 0x0020;
        private const uint PROCESS_VM_OPERATION = 0x0008;

        private IntPtr processHandle = IntPtr.Zero;
        private Process gameProcess = null;
        private bool isAimbotRunning = false;
        private CancellationTokenSource cancellationToken;

        public AimbotSettings Settings { get; private set; } = new AimbotSettings();

        public bool FindAndAttachToGame()
        {
            try
            {
                Process[] processes = Process.GetProcesses();
                foreach (var proc in processes)
                {
                    try
                    {
                        string procName = proc.ProcessName.ToLower();
                        if (procName.Contains("cube") || procName.Contains("assaultcube") || procName.Contains("ac"))
                        {
                            gameProcess = proc;
                            processHandle = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, false, (uint)proc.Id);
                            return processHandle != IntPtr.Zero;
                        }
                    }
                    catch { }
                }
                return false;
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error finding game: {ex.Message}");
                return false;
            }
        }

        public void StartAimbot()
        {
            if (isAimbotRunning) return;

            isAimbotRunning = true;
            cancellationToken = new CancellationTokenSource();
            Settings.Enabled = true;

            Task.Run(() => AimbotLoop(cancellationToken.Token));
        }

        public void StopAimbot()
        {
            isAimbotRunning = false;
            Settings.Enabled = false;
            cancellationToken?.Cancel();

            if (processHandle != IntPtr.Zero)
            {
                CloseHandle(processHandle);
                processHandle = IntPtr.Zero;
            }
        }

        private async Task AimbotLoop(CancellationToken token)
        {
            while (!token.IsCancellationRequested && isAimbotRunning)
            {
                try
                {
                    if (!Settings.Enabled)
                    {
                        await Task.Delay(100, token);
                        continue;
                    }

                    var player = GetPlayerInfo(0);
                    if (player == null || !player.IsAlive)
                    {
                        await Task.Delay(10, token);
                        continue;
                    }

                    if (Settings.OnlyOnCrouch && !player.IsCrouching)
                    {
                        await Task.Delay(10, token);
                        continue;
                    }

                    var enemy = GetClosestEnemy(player.Team, player.HeadPosition, 0);
                    if (enemy != null)
                    {
                        SnapToEnemy(player, enemy);
                    }

                    await Task.Delay(10, token);
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Aimbot loop error: {ex.Message}");
                    await Task.Delay(100, token);
                }
            }
        }

        public PlayerInfo GetPlayerInfo(int playerIndex)
        {
            try
            {
                if (processHandle == IntPtr.Zero) return null;

                const int PLAYER_OFFSET = 0x0010F4F4;
                const float HEAD_HEIGHT = 1.7f;
                const int POS_X = 0x0;
                const int POS_Y = 0x4;
                const int POS_Z = 0x8;
                const int HEALTH = 0xF8;
                const int ARMOR = 0xFC;
                const int CROUCHING = 0x21C;
                const int TEAM = 0x30;

                var player = new PlayerInfo { Index = playerIndex };

                IntPtr playerPtr = new IntPtr(PLAYER_OFFSET + (playerIndex * 0x4));

                player.Position.X = ReadFloat(playerPtr + POS_X);
                player.Position.Y = ReadFloat(playerPtr + POS_Y);
                player.Position.Z = ReadFloat(playerPtr + POS_Z);

                player.HeadPosition = new Vector3(
                    player.Position.X,
                    player.Position.Y,
                    player.Position.Z + HEAD_HEIGHT
                );

                player.Health = ReadInt(playerPtr + HEALTH);
                player.Armor = ReadInt(playerPtr + ARMOR);
                player.IsCrouching = ReadByte(playerPtr + CROUCHING) != 0;
                player.Team = ReadByte(playerPtr + TEAM);
                player.IsAlive = player.Health > 0;

                return player;
            }
            catch
            {
                return null;
            }
        }

        private PlayerInfo GetClosestEnemy(int playerTeam, Vector3 playerPos, int playerIndex)
        {
            try
            {
                float closestDistance = float.MaxValue;
                PlayerInfo closestEnemy = null;

                const int MAX_PLAYERS = 128;

                for (int i = 0; i < MAX_PLAYERS; i++)
                {
                    if (i == playerIndex) continue;

                    var enemy = GetPlayerInfo(i);
                    if (enemy == null) continue;

                    if (Settings.DeadCheck && !enemy.IsAlive) continue;
                    if (Settings.TeamCheck && enemy.Team == playerTeam) continue;
                    if (Settings.HealthCheck && enemy.Health <= 0) continue;

                    float distance = playerPos.DistanceTo(enemy.HeadPosition);

                    if (distance > Settings.MaxDistance) continue;

                    if (distance < closestDistance)
                    {
                        closestDistance = distance;
                        closestEnemy = enemy;
                    }
                }

                return closestEnemy;
            }
            catch
            {
                return null;
            }
        }

        private void SnapToEnemy(PlayerInfo player, PlayerInfo enemy)
        {
            try
            {
                float dx = enemy.HeadPosition.X - player.HeadPosition.X;
                float dy = enemy.HeadPosition.Y - player.HeadPosition.Y;
                float dz = enemy.HeadPosition.Z - player.HeadPosition.Z;

                float yaw = (float)Math.Atan2(dy, dx);
                float distanceXY = (float)Math.Sqrt(dx * dx + dy * dy);
                float pitch = distanceXY > 0 ? (float)Math.Atan2(dz, distanceXY) : 0;

                const int PLAYER_OFFSET = 0x0010F4F4;
                const int CAMERA_YAW = 0x40;
                const int CAMERA_PITCH = 0x44;

                IntPtr yawPtr = new IntPtr(PLAYER_OFFSET + CAMERA_YAW);
                IntPtr pitchPtr = new IntPtr(PLAYER_OFFSET + CAMERA_PITCH);

                WriteFloat(yawPtr, yaw);
                WriteFloat(pitchPtr, pitch);

                Debug.WriteLine($"🎯 Snap: Enemy {enemy.Index} | Distance: {player.HeadPosition.DistanceTo(enemy.HeadPosition):F1}m");
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Snap error: {ex.Message}");
            }
        }

        private float ReadFloat(IntPtr address)
        {
            byte[] buffer = new byte[4];
            if (ReadProcessMemory(processHandle, address, buffer, 4, out _))
            {
                return BitConverter.ToSingle(buffer, 0);
            }
            return 0;
        }

        private int ReadInt(IntPtr address)
        {
            byte[] buffer = new byte[4];
            if (ReadProcessMemory(processHandle, address, buffer, 4, out _))
            {
                return BitConverter.ToInt32(buffer, 0);
            }
            return 0;
        }

        private byte ReadByte(IntPtr address)
        {
            byte[] buffer = new byte[1];
            if (ReadProcessMemory(processHandle, address, buffer, 1, out _))
            {
                return buffer[0];
            }
            return 0;
        }

        private void WriteFloat(IntPtr address, float value)
        {
            byte[] buffer = BitConverter.GetBytes(value);
            WriteProcessMemory(processHandle, address, buffer, 4, out _);
        }

        private void WriteInt(IntPtr address, int value)
        {
            byte[] buffer = BitConverter.GetBytes(value);
            WriteProcessMemory(processHandle, address, buffer, 4, out _);
        }
    }
}
