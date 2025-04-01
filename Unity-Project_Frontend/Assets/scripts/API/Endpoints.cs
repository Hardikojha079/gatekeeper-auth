namespace API
{
    public static class Endpoints
    {
        private const string BaseURL = "http://localhost:5000";
        
        public const string Register = BaseURL + "/register";
        public const string Login = BaseURL + "/login";
        public const string Profile = BaseURL + "/profile";
        public const string AllUsers = BaseURL + "/";

        public static string GetUserEndpoint(string accountNumber)
        {
            return BaseURL + "/" + accountNumber;
        }
    }
}
