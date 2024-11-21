// Форматирование денежных сумм
const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 2
    }).format(amount);
};

// Форматирование даты
const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
};

// Обработка формы перевода
const handleTransfer = async (event) => {
    event.preventDefault();
    const form = event.target;
    const recipient = form.querySelector('[name="recipient"]').value;
    const amount = parseFloat(form.querySelector('[name="amount"]').value);

    if (!recipient || !amount || amount <= 0) {
        showNotification('Пожалуйста, заполните все поля корректно', 'error');
        return;
    }

    try {
        // В реальном приложении здесь будет API-запрос
        showNotification('Перевод выполнен успешно!', 'success');
        form.reset();
        updateBalance();
        updateTransactionHistory();
    } catch (error) {
        showNotification('Ошибка при выполнении перевода', 'error');
    }
};

// Уведомления
const showNotification = (message, type = 'info') => {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Анимация появления
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    // Автоматическое скрытие
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
};

// Обновление баланса
const updateBalance = async () => {
    const balanceElement = document.querySelector('.balance-amount');
    if (!balanceElement) return;

    try {
        // В реальном приложении здесь будет API-запрос
        const balance = 150000; // Пример значения
        balanceElement.textContent = formatCurrency(balance);
    } catch (error) {
        console.error('Ошибка при обновлении баланса:', error);
    }
};

// Обновление истории транзакций
const updateTransactionHistory = async () => {
    const transactionsList = document.querySelector('.transactions-list');
    if (!transactionsList) return;

    try {
        // В реальном приложении здесь будет API-запрос
        const transactions = [
            { id: 1, type: 'out', amount: 5000, recipient: 'Иван', date: '2024-03-20T15:30:00' },
            { id: 2, type: 'in', amount: 15000, sender: 'Петр', date: '2024-03-19T12:15:00' },
            { id: 3, type: 'out', amount: 3000, recipient: 'Анна', date: '2024-03-18T09:45:00' }
        ];

        transactionsList.innerHTML = transactions.map(transaction => `
            <div class="transaction-item">
                <div class="transaction-info">
                    <div class="transaction-user">
                        ${transaction.type === 'out' 
                            ? `Перевод ${transaction.recipient}` 
                            : `Получено от ${transaction.sender}`}
                    </div>
                    <div class="transaction-date">${formatDate(transaction.date)}</div>
                </div>
                <div class="transaction-amount ${transaction.type === 'in' ? 'positive' : 'negative'}">
                    ${transaction.type === 'in' ? '+' : '-'}${formatCurrency(transaction.amount)}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Ошибка при обновлении истории транзакций:', error);
    }
};

// Обработчик выхода из системы
const handleLogout = () => {
    // В реальном приложении здесь будет очистка сессии
    window.location.href = 'login.html';
};

// Обработчик для кнопки показать/скрыть пасскод
const initPasscodeToggle = () => {
    const showPasscodeBtn = document.getElementById('showPasscode');
    if (showPasscodeBtn) {
        showPasscodeBtn.addEventListener('click', () => {
            const passcodeInput = showPasscodeBtn.parentElement.querySelector('input');
            if (passcodeInput.type === 'password') {
                passcodeInput.type = 'text';
                showPasscodeBtn.textContent = 'Скрыть';
            } else {
                passcodeInput.type = 'password';
                showPasscodeBtn.textContent = 'Показать';
            }
        });
    }
};

// Обработчик фильтров транзакций
const initTransactionFilters = () => {
    const filterSelect = document.querySelector('.filter-select');
    const filterDate = document.querySelector('.filter-date');

    if (filterSelect && filterDate) {
        filterSelect.addEventListener('change', updateTransactionHistory);
        filterDate.addEventListener('change', updateTransactionHistory);
    }
};

// Обновляем инициализацию при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Инициализация форм
    const transferForm = document.querySelector('.transfer-form');
    if (transferForm) {
        transferForm.addEventListener('submit', handleTransfer);
    }

    // Инициализация кнопки выхода
    const logoutButton = document.querySelector('.logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }

    // Обновление данных при загрузке
    updateBalance();
    updateTransactionHistory();

    // Автоматическое обновление данных каждые 30 секунд
    setInterval(() => {
        updateBalance();
        updateTransactionHistory();
    }, 30000);

    initPasscodeToggle();
    initTransactionFilters();
});

// Добавляем стили для уведомлений
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 4px;
        background: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transform: translateX(120%);
        transition: transform 0.3s ease;
        z-index: 1000;
    }

    .notification.show {
        transform: translateX(0);
    }

    .notification.success {
        background: var(--secondary-color);
        color: white;
    }

    .notification.error {
        background: #e74c3c;
        color: white;
    }

    .notification.info {
        background: var(--primary-color);
        color: white;
    }
`;

document.head.appendChild(style);
