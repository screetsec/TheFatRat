// C#
using System.Runtime.InteropServices;
namespace pshcmd
{
	public class CMD
	{
		[DllImport("msvcrt.dll")]
		public static extern int system(string cmd);
		public static void Main()
		{
			system("PAYLOAD");
		}
	}
}
