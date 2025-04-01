namespace API.Models
{
    [System.Serializable]
    public class RegisterRequest
    {
        public string account_number, first_name, last_name, gender, phone_number, address, bank_account_type, date_of_account_opening, branch_code, password;
        public int age;
        public RegisterRequest(string accountNumber, string firstName, string lastName, int age, string gender, string phoneNumber, string address, string bankAccountType, string dateOfAccountOpening, string branchCode, string password)
        {
            this.account_number = accountNumber;
            this.first_name = firstName;
            this.last_name = lastName;
            this.age = age;
            this.gender = gender;
            this.phone_number = phoneNumber;
            this.address = address;
            this.bank_account_type = bankAccountType;
            this.date_of_account_opening = dateOfAccountOpening;
            this.branch_code = branchCode;
            this.password = password;
        }
    }

    [System.Serializable]
    public class LoginRequest
    {
        public string account_number, password;
        public LoginRequest(string accountNumber, string password)
        {
            this.account_number = accountNumber;
            this.password = password;
        }
    }

    [System.Serializable]
    public class LoginResponse
    {
        public bool success;
        public string token;
        public string message;
    }

    [System.Serializable]
    public class UserUpdateRequest
    {
        public string first_name, last_name, phone_number, address;
        public int age;
        public UserUpdateRequest(string firstName, string lastName, int age, string phoneNumber, string address)
        {
            this.first_name = firstName;
            this.last_name = lastName;
            this.age = age;
            this.phone_number = phoneNumber;
            this.address = address;
        }
    }
}
