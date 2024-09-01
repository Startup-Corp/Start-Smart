async function getBalance() {
  await fetch("/get_balance_user", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.user_data.balance);
      console.log(data.user_data.balance2);
    // Обновляем баланс для тарифов
    document.getElementById(
      "balance-chat-gpt"
    ).textContent = `${data.user_data.balance} R`;
    document.getElementById(
      "balance-expert"
    ).textContent = `${data.user_data.balance2} R`;
  })
  .catch((error) => {
    console.error("Ошибка при получении баланса:", error);
  });
}

// Вызов getBalance при загрузке страницы
window.onload = getBalance;