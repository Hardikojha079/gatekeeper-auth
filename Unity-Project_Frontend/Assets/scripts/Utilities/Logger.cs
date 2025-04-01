using UnityEngine;

namespace Utilities
{
    public static class Logger
    {
        public static void Log(string message)
        {
            Debug.Log($"[LOG] {message}");
        }

        public static void LogError(string message)
        {
            Debug.LogError($"[ERROR] {message}");
        }
    }
}
