import { test, expect } from '@playwright/test';

// Szablon testu E2E w Playwright dla ścieżek krytycznych interfejsu UI

test.describe('Dashboard E2E Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('powinien zalogować i wyświetlić statystyki', async ({ page }) => {
    // 1. Logowanie
    await page.fill('#username', 'admin');
    await page.fill('#password', 'admin');
    await page.click('button[type="submit"]');

    // 2. Weryfikacja kontenera głównego aplikacji
    const appContainer = page.locator('#app-container');
    await expect(appContainer).toBeVisible();

    // 3. Sprawdzenie renderowania wykresu
    const chart = page.locator('#analytics-chart-container');
    await expect(chart).toBeVisible();
  });
});
