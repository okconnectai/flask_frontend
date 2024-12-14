document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('meusDadosForm');
    const saveButton = document.getElementById('saveButton');
    const inputs = form.querySelectorAll('input, textarea');
    
    // Mostrar/ocultar botão de salvar
    const toggleSaveButton = () => {
        let hasChanges = false;
        inputs.forEach(input => {
            if (input.value !== input.defaultValue) {
                hasChanges = true;
            }
        });
        saveButton.classList.toggle('show', hasChanges);
    };

    // Adicionar eventos para detectar mudanças
    inputs.forEach(input => {
        input.addEventListener('input', toggleSaveButton);
        input.addEventListener('change', toggleSaveButton);
    });

    // Submeter formulário principal
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            whatsapp: document.getElementById('whatsapp').value,
            cpf_cnpj: document.getElementById('cpf_cnpj').value,
            company_name: document.getElementById('company_name').value,
            niche: document.getElementById('niche').value,
            goals: document.getElementById('goals').value
        };

        try {
            const response = await fetch('/api/update-profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            
            if (response.ok) {
                // Atualizar valores padrão dos campos
                inputs.forEach(input => {
                    input.defaultValue = input.value;
                });
                
                // Esconder botão de salvar
                saveButton.classList.remove('show');
                
                // Mostrar mensagem de sucesso
                const alert = document.createElement('div');
                alert.className = 'alert alert-success alert-dismissible fade show';
                alert.innerHTML = `
                    Dados atualizados com sucesso!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                form.insertBefore(alert, form.firstChild);
                
                // Remover alerta após 3 segundos
                setTimeout(() => {
                    alert.remove();
                }, 3000);
            } else {
                throw new Error(data.message || 'Erro ao atualizar dados');
            }
        } catch (error) {
            console.error('Erro:', error);
            const alert = document.createElement('div');
            alert.className = 'alert alert-danger alert-dismissible fade show';
            alert.innerHTML = `
                ${error.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            form.insertBefore(alert, form.firstChild);
        }
    });

    // Máscara para WhatsApp
    const whatsappInput = document.getElementById('whatsapp');
    whatsappInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 11) value = value.slice(0, 11);
        if (value.length > 0) {
            value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
        }
        e.target.value = value;
    });

    // Máscara para CPF/CNPJ
    const cpfCnpjInput = document.getElementById('cpf_cnpj');
    cpfCnpjInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) { // CPF
            if (value.length > 11) value = value.slice(0, 11);
            if (value.length > 9) {
                value = `${value.slice(0, 3)}.${value.slice(3, 6)}.${value.slice(6, 9)}-${value.slice(9)}`;
            } else if (value.length > 6) {
                value = `${value.slice(0, 3)}.${value.slice(3, 6)}.${value.slice(6)}`;
            } else if (value.length > 3) {
                value = `${value.slice(0, 3)}.${value.slice(3)}`;
            }
        } else { // CNPJ
            if (value.length > 14) value = value.slice(0, 14);
            if (value.length > 12) {
                value = `${value.slice(0, 2)}.${value.slice(2, 5)}.${value.slice(5, 8)}/${value.slice(8, 12)}-${value.slice(12)}`;
            } else if (value.length > 8) {
                value = `${value.slice(0, 2)}.${value.slice(2, 5)}.${value.slice(5, 8)}/${value.slice(8)}`;
            } else if (value.length > 5) {
                value = `${value.slice(0, 2)}.${value.slice(2, 5)}.${value.slice(5)}`;
            } else if (value.length > 2) {
                value = `${value.slice(0, 2)}.${value.slice(2)}`;
            }
        }
        e.target.value = value;
    });

    // Formulário de alteração de senha
    const changePasswordForm = document.getElementById('changePasswordForm');
    changePasswordForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (newPassword !== confirmPassword) {
            alert('As senhas não coincidem!');
            return;
        }

        try {
            const response = await fetch('/api/change-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    currentPassword: document.getElementById('currentPassword').value,
                    newPassword: newPassword
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                modal.hide();
                
                // Limpar formulário
                changePasswordForm.reset();
                
                // Mostrar mensagem de sucesso
                const alert = document.createElement('div');
                alert.className = 'alert alert-success alert-dismissible fade show';
                alert.innerHTML = `
                    Senha alterada com sucesso!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                form.insertBefore(alert, form.firstChild);
                
                // Remover alerta após 3 segundos
                setTimeout(() => {
                    alert.remove();
                }, 3000);
            } else {
                throw new Error(data.message || 'Erro ao alterar senha');
            }
        } catch (error) {
            console.error('Erro:', error);
            const alert = document.createElement('div');
            alert.className = 'alert alert-danger alert-dismissible fade show';
            alert.innerHTML = `
                ${error.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            changePasswordForm.insertBefore(alert, changePasswordForm.firstChild);
        }
    });
});
