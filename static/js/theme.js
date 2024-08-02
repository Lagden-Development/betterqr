document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.querySelector(".theme-toggle button");
  const icon = themeToggle.querySelector("i");

  function setDarkMode(isDark) {
    if (isDark) {
      document.documentElement.classList.add("dark");
      icon.classList.remove("fa-moon");
      icon.classList.add("fa-sun");
    } else {
      document.documentElement.classList.remove("dark");
      icon.classList.remove("fa-sun");
      icon.classList.add("fa-moon");
    }
  }

  // Load initial theme
  let isDarkMode = localStorage.getItem("dark-mode");
  if (isDarkMode === null) {
    // Check system preference if localStorage item doesn't exist
    isDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
  } else {
    isDarkMode = isDarkMode === "true";
  }
  setDarkMode(isDarkMode);

  themeToggle.addEventListener("click", () => {
    const isDarkMode = document.documentElement.classList.toggle("dark");
    localStorage.setItem("dark-mode", isDarkMode);
    setDarkMode(isDarkMode);
  });
});
