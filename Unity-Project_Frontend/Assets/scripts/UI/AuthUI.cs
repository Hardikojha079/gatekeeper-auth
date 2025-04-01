using UnityEngine;
using UnityEngine.UI;
using API;
using API.Models;

public class AuthUI : MonoBehaviour
{
    public InputField loginAccountNumberInput, loginPasswordInput;
    public InputField regAccountNumberInput, regFirstNameInput, regLastNameInput, regAgeInput, regGenderInput, regPhoneNumberInput, regAddressInput, regBankAccountTypeInput, regDateOfAccountOpeningInput, regBranchCodeInput, regPasswordInput;
    public Text responseText;
    
    private APIManager apiManager;

    private void Start()
    {
        apiManager = gameObject.AddComponent<APIManager>();
    }

    public void OnLogin()
    {
        apiManager.Login(new LoginRequest(loginAccountNumberInput.text, loginPasswordInput.text), response => responseText.text = response);
    }

    public void OnRegister()
    {
        apiManager.Register(new RegisterRequest(regAccountNumberInput.text, regFirstNameInput.text, regLastNameInput.text, int.Parse(regAgeInput.text), regGenderInput.text, regPhoneNumberInput.text, regAddressInput.text, regBankAccountTypeInput.text, regDateOfAccountOpeningInput.text, regBranchCodeInput.text, regPasswordInput.text), response => responseText.text = response);
    }
}
