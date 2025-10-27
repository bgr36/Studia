document.addEventListener("DOMContentLoaded", () => {
  const bodyClasses = document.body.classList;
  const navLinks = document.querySelectorAll("nav a");

  navLinks.forEach(link => {
    for (const cls of bodyClasses) {
      if (link.classList.contains(cls)) {
        link.classList.add("active");
      }
    }
  });

  const toggleButton = document.getElementById("menu-toggle");
  const navMenu = document.querySelector("nav ul");

  toggleButton.addEventListener("click", () => {
    navMenu.classList.toggle("show");
  });
});