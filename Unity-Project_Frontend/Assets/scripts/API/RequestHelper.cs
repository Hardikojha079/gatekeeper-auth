using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace API
{
    public static class RequestHelper
    {
        public static IEnumerator PostRequest(string url, string jsonData, System.Action<string> callback)
        {
            using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
            {
                byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");

                yield return request.SendWebRequest();

                callback(request.downloadHandler.text);
            }
        }

        public static IEnumerator GetRequest(string url, string token, System.Action<string> callback)
        {
            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                request.SetRequestHeader("Authorization", $"Bearer {token}");
                yield return request.SendWebRequest();

                callback(request.downloadHandler.text);
            }
        }

        public static IEnumerator PutRequest(string url, string jsonData, string token, System.Action<string> callback)
        {
            using (UnityWebRequest request = UnityWebRequest.Put(url, jsonData))
            {
                request.uploadHandler = new UploadHandlerRaw(System.Text.Encoding.UTF8.GetBytes(jsonData));
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");
                request.SetRequestHeader("Authorization", $"Bearer {token}");

                yield return request.SendWebRequest();

                callback(request.downloadHandler.text);
            }
        }

        public static IEnumerator DeleteRequest(string url, string token, System.Action<string> callback)
        {
            using (UnityWebRequest request = UnityWebRequest.Delete(url))
            {
                request.SetRequestHeader("Authorization", $"Bearer {token}");
                yield return request.SendWebRequest();

                callback(request.downloadHandler.text);
            }
        }
    }
}
