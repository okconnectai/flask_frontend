document.addEventListener('DOMContentLoaded', function () {
    // Get all form inputs
    const whatsappInput = document.querySelector('input[name="whatsapp"]');
    const cpfCnpjInput = document.querySelector('input[name="cpf_cnpj"]');
    const emailInput = document.querySelector('input[name="email"]');
    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const accountNameInput = document.querySelector('input[name="account_name"]');
    const nicheInput = document.querySelector('input[name="niche"]');
    const goalsInput = document.querySelector('textarea[name="goals"]');
    const nameInput = document.querySelector('input[name="name"]');
    const forgotPasswordEmailInput = document.querySelector('input[name="forgot_password_email"]');

    // Remove HTML5 validation
    document.querySelectorAll('form').forEach(form => {
        form.setAttribute('novalidate', true);
    });

    // Email pattern for validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordPattern = /^.{8,}$/;

    // Validate email fields
    function validateEmail(input) {
        const value = input.value.trim();
        if (value === '') {
            console.log('O campo de email não pode ficar em branco.');
            input.focus();
            return false;
        } else if (!emailPattern.test(value)) {
            console.log('Por favor, insira um email válido.');
            input.focus();
            return false;
        }
        return true;
    }

    // Add email validation to all email fields
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });
    }

    if (usernameInput) {
        usernameInput.addEventListener('blur', function() {
            validateEmail(this);
        });
    }

    if (forgotPasswordEmailInput) {
        forgotPasswordEmailInput.addEventListener('blur', function() {
            validateEmail(this);
        });
    }

    // Apply mask to WhatsApp field
    if (whatsappInput) {
        whatsappInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            e.target.value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        });

        whatsappInput.addEventListener('blur', function () {
            const value = this.value.replace(/\D/g, '');
            if (value.length !== 11) {
                console.log('Por favor, insira um número de WhatsApp válido com DDD.');
                this.focus();
            }
        });
    }

    // Apply mask to CPF/CNPJ field
    if (cpfCnpjInput) {
        cpfCnpjInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                e.target.value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            } else {
                e.target.value = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
            }
        });

        cpfCnpjInput.addEventListener('blur', function () {
            const value = this.value.replace(/\D/g, '');
            if (value.length !== 11 && value.length !== 14) {
                console.log('Por favor, insira um CPF ou CNPJ válido.');
                this.focus();
            }
        });
    }

    // Password validation
    if (passwordInput) {
        passwordInput.addEventListener('blur', function () {
            const value = this.value;
            if (value === '') {
                console.log('O campo de senha não pode ficar em branco.');
                this.focus();
            } else if (!passwordPattern.test(value)) {
                console.log('A senha deve ter no mínimo 8 caracteres, letras maiúsculas, minúsculas, números e caracteres especiais.');
                this.focus();
            }
        });
    }

    // Format and validate non-null fields
    function formatAndValidateNonNull(input, fieldName) {
        let value = input.value.trim();
        if (value === '') {
            console.log(`O campo ${fieldName} não pode ficar em branco.`);
            input.focus();
            return false;
        }
        value = value.toLowerCase().replace(/\b\w/g, char => char.toUpperCase());
        input.value = value;
        return true;
    }

    // Apply validation to name, account_name, and niche
    if (nameInput) {
        nameInput.addEventListener('blur', function () {
            formatAndValidateNonNull(this, 'Nome');
        });
    }

    if (accountNameInput) {
        accountNameInput.addEventListener('blur', function () {
            formatAndValidateNonNull(this, 'Nome da Empresa');
        });
    }

    if (nicheInput) {
        nicheInput.addEventListener('blur', function () {
            formatAndValidateNonNull(this, 'Nicho');
        });
    }

    // Goals validation
    if (goalsInput) {
        goalsInput.addEventListener('blur', function () {
            const value = this.value.trim();
            if (value === '') {
                console.log('O campo de objetivos não pode ficar em branco.');
                this.focus();
            } else if (value.length < 100) {
                console.log('Descreva melhor seus objetivos. É necessário no mínimo 100 caracteres.');
                this.focus();
            }
        });
    }

    // Form submit validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            const invalidFields = form.querySelectorAll(':invalid');
            if (invalidFields.length > 0) {
                event.preventDefault();
                invalidFields.forEach(field => {
                    const label = form.querySelector(`label[for="${field.id}"]`).innerText;
                    console.log(`${label}: ${field.validationMessage}`);
                    field.focus();
                    return false;
                });
            } else {
                // Prevent default form submission
                event.preventDefault();
                
                const inputs = form.querySelectorAll('input, textarea');
                let isValid = true;

                inputs.forEach(input => {
                    if (input.type === 'email' || input.name === 'username') {
                        isValid = validateEmail(input) && isValid;
                    } else if (input.type === 'password') {
                        const value = input.value;
                        if (value === '') {
                            console.log('O campo de senha não pode ficar em branco.');
                            input.focus();
                            isValid = false;
                        } else if (!passwordPattern.test(value)) {
                            console.log('A senha deve ter no mínimo 8 caracteres.');
                            input.focus();
                            isValid = false;
                        }
                    } else if (input.name === 'goals') {
                        const value = input.value.trim();
                        if (value === '') {
                            console.log('O campo de objetivos não pode ficar em branco.');
                            input.focus();
                            isValid = false;
                        } else if (value.length < 50) {
                            console.log('Descreva melhor seus objetivos. É necessário no mínimo 50 caracteres.');
                            input.focus();
                            isValid = false;
                        }
                    } else if (input.required && input.value.trim() === '') {
                        console.log(`O campo ${input.name} não pode ficar em branco.`);
                        input.focus();
                        isValid = false;
                    }
                });

                // If all validations pass, submit the form
                if (isValid) {
                    HTMLFormElement.prototype.submit.call(form);
                }
            }
        });
    });
});
