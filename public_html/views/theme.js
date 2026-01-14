/**
 * Shared Theme Logic for WikiProject Medicine Dashboard
 */

/**
 * @param {Function|null} reloadChart
 */
function toggleTheme(reloadChart = null) {
    const html = document.documentElement;
    const currentTheme = html.getAttribute("data-theme") || "light";
    const newTheme = currentTheme === "light" ? "dark" : "light";

    html.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeIcons(newTheme);

    // Optional callback to refresh charts
    if (reloadChart && typeof reloadChart === "function") {
        reloadChart();
    }
}

/**
 * @param {string} theme
 */
function updateThemeIcons(theme) {
    const moon = document.querySelector(".dark-icon");
    const sun = document.querySelector(".light-icon");
    if (!moon || !sun) return;

    if (theme === "dark") {
        moon.classList.add("d-none");
        sun.classList.remove("d-none");
    } else {
        moon.classList.remove("d-none");
        sun.classList.add("d-none");
    }
}

// Initial sync for icons
document.addEventListener("DOMContentLoaded", () => {
    updateThemeIcons(localStorage.getItem("theme") || "light");
});
