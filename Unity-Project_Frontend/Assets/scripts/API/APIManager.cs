using System.Collections;
using UnityEngine;
using API.Models;
using System;

namespace API
{
    public class APIManager : MonoBehaviour
    {
        private string jwtToken;

        private void Start()
        {
            jwtToken = PlayerPrefs.GetString("authToken", "");
        }

        public void Register(RegisterRequest request, Action<string> callback)
        {
            string jsonData = JsonUtility.ToJson(request);
            StartCoroutine(RequestHelper.PostRequest(Endpoints.Register, jsonData, callback));
        }

        public void Login(LoginRequest request, Action<string> callback)
        {
            string jsonData = JsonUtility.ToJson(request);
            StartCoroutine(RequestHelper.PostRequest(Endpoints.Login, jsonData, (response) =>
            {
                try
                {
                    var loginResponse = JsonUtility.FromJson<LoginResponse>(response);
                    if (loginResponse.success && !string.IsNullOrEmpty(loginResponse.token))
                    {
                        jwtToken = loginResponse.token;
                        PlayerPrefs.SetString("authToken", jwtToken);
                        callback("Login successful! Token saved.");
                    }
                    else
                    {
                        callback($"Login failed: {loginResponse.message}");
                    }
                }
                catch (Exception ex)
                {
                    callback($"Login failed. Error: {ex.Message}");
                }
            }));
        }

        public void FetchProfile(Action<string> callback)
        {
            if (string.IsNullOrEmpty(jwtToken))
            {
                callback("No token available. Please log in first.");
                return;
            }
            StartCoroutine(RequestHelper.GetRequest(Endpoints.Profile, jwtToken, callback));
        }

        public void UpdateUser(string accountNumber, UserUpdateRequest updatedData, Action<string> callback)
        {
            if (string.IsNullOrEmpty(jwtToken))
            {
                callback("No token available. Please log in first.");
                return;
            }
            string jsonData = JsonUtility.ToJson(updatedData);
            StartCoroutine(RequestHelper.PutRequest(Endpoints.GetUserEndpoint(accountNumber), jsonData, jwtToken, callback));
        }

        public void DeleteUser(string accountNumber, Action<string> callback)
        {
            if (string.IsNullOrEmpty(jwtToken))
            {
                callback("No token available. Please log in first.");
                return;
            }
            StartCoroutine(RequestHelper.DeleteRequest(Endpoints.GetUserEndpoint(accountNumber), jwtToken, callback));
        }

        public void FetchAllUsers(Action<string> callback)
        {
            if (string.IsNullOrEmpty(jwtToken))
            {
                callback("No token available. Please log in first.");
                return;
            }
            StartCoroutine(RequestHelper.GetRequest(Endpoints.AllUsers, jwtToken, callback));
        }

        public void ClearToken()
        {
            jwtToken = null;
            PlayerPrefs.DeleteKey("authToken");
        }
    }
}
