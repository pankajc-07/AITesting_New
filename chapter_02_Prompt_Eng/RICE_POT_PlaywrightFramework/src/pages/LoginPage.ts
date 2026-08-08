import { Page, Locator } from '@playwright/test';

/**
 * Page Object Model for the Salesforce login page.
 * Encapsulates all element locators and user actions for the login form.
 * Uses Playwright's built-in semantic locators (getByLabel, getByRole, getByText)
 * for resilient element selection, with xpath as a fallback for dynamic elements.
 *
 * Real DOM verified on: https://login.salesforce.com/?locale=in as of 2026-08-08
 */
export class LoginPage {
    /** Locator for the username/email input field (labeled 'Username' in Salesforce DOM) */
    private usernameField: Locator;

    /** Locator for the password input field */
    private passwordField: Locator;

    /** Locator for the Log In submit button */
    private loginButton: Locator;

    /** Locator for the Remember Me checkbox */
    private rememberMeCheckbox: Locator;

    /** Locator for the error message container — uses role='alert' for standard Salesforce error blocks */
    private errorMessage: Locator;

    /** Locator for the page heading to verify page load */
    private pageHeading: Locator;

    /** Locator for the Forgot Your Password link */
    private forgotPasswordLink: Locator;

    /** Locator for the Use Custom Domain link */
    private useCustomDomainLink: Locator;

    constructor(private page: Page) {
        this.usernameField = this.page.getByLabel('Username');
        this.passwordField = this.page.getByLabel('Password');
        this.loginButton = this.page.getByRole('button', { name: 'Log In' });
        this.rememberMeCheckbox = this.page.getByRole('checkbox', { name: 'Remember me' });
        this.errorMessage = this.page.locator('xpath=//div[contains(@class,"loginError")]');
        this.pageHeading = this.page.getByRole('heading', { name: 'Salesforce login', level: 1 });
        this.forgotPasswordLink = this.page.getByRole('link', { name: 'Forgot Your Password?' });
        this.useCustomDomainLink = this.page.getByRole('link', { name: 'Use Custom Domain' });
    }

    /**
     * Navigates directly to the Salesforce login page.
     * Should only be used for explicit navigation scenarios; the base fixture handles normal navigation.
     * @param url - Optional override URL for staging environments
     */
    async navigateToLogin(url?: string): Promise<void> {
        const targetUrl = url || 'https://login.salesforce.com/?locale=in';
        try {
            await this.page.goto(targetUrl, { waitUntil: 'networkidle' });
            await this.page.waitForLoadState('domcontentloaded');
        } catch (error) {
            throw new Error(`Failed to navigate to Salesforce login page: ${error}`);
        }
    }

    /**
     * Enters the provided text into the username field, clearing any existing value first.
     * @param username - The username or email to enter
     */
    async enterUsername(username: string): Promise<void> {
        try {
            await this.usernameField.clear();
            await this.usernameField.fill(username);
        } catch (error) {
            throw new Error(`Failed to enter username: ${error}`);
        }
    }

    /**
     * Enters the provided text into the password field, clearing any existing value first.
     * @param password - The password to enter
     */
    async enterPassword(password: string): Promise<void> {
        try {
            await this.passwordField.clear();
            await this.passwordField.fill(password);
        } catch (error) {
            throw new Error(`Failed to enter password: ${error}`);
        }
    }

    /**
     * Clicks the Log In button to submit the login form.
     */
    async clickLogin(): Promise<void> {
        try {
            await this.loginButton.click();
        } catch (error) {
            throw new Error(`Failed to click login button: ${error}`);
        }
    }

    /**
     * Performs a complete login flow: fills username, password, and clicks submit.
     * This is the primary convenience method for valid-login scenarios.
     * @param user - The username/email to use
     * @param pass - The password to use
     */
    async doLogin(user: string, pass: string): Promise<void> {
        try {
            await this.enterUsername(user);
            await this.enterPassword(pass);
            await this.clickLogin();
        } catch (error) {
            throw new Error(`Login attempt failed: ${error}`);
        }
    }

    /**
     * Retrieves the text content of the error message displayed on invalid login.
     * Waits for the error element to become visible before reading its text.
     * @returns The error message string, or empty string if none is displayed
     */
    async getErrorMessage(): Promise<string> {
        try {
            await this.errorMessage.waitFor({ state: 'visible', timeout: 10000 });
            return (await this.errorMessage.textContent()) || '';
        } catch {
            return '';
        }
    }

    /**
     * Checks whether an error message is currently displayed on the login page.
     * @returns true if the error message element is visible, false otherwise
     */
    async isErrorMessageDisplayed(): Promise<boolean> {
        try {
            return await this.errorMessage.isVisible();
        } catch {
            return false;
        }
    }

    /**
     * Toggles the Remember Me checkbox to the desired state.
     * @param checked - true to check the box, false to uncheck
     */
    async setRememberMe(checked: boolean): Promise<void> {
        try {
            const isCurrentlyChecked = await this.rememberMeCheckbox.isChecked();
            if (isCurrentlyChecked !== checked) {
                await this.rememberMeCheckbox.click();
            }
        } catch (error) {
            throw new Error(`Failed to toggle Remember Me checkbox: ${error}`);
        }
    }

    /**
     * Checks whether the Remember Me checkbox is currently selected.
     * @returns true if checked, false otherwise
     */
    async isRememberMeChecked(): Promise<boolean> {
        try {
            return await this.rememberMeCheckbox.isChecked();
        } catch {
            return false;
        }
    }

    /**
     * Clears both the username and password fields.
     * Useful for resetting form state between test cases.
     */
    async clearFields(): Promise<void> {
        try {
            await this.usernameField.clear();
            await this.passwordField.clear();
        } catch (error) {
            throw new Error(`Failed to clear form fields: ${error}`);
        }
    }

    /**
     * Verifies that the login page has fully loaded by checking the presence
     * of all critical UI elements: username field, password field, login button, and heading.
     * @returns true if all elements are visible, false otherwise
     */
    async isPageLoaded(): Promise<boolean> {
        try {
            const headingVisible = await this.pageHeading.isVisible();
            const usernameVisible = await this.usernameField.isVisible();
            const passwordVisible = await this.passwordField.isVisible();
            const loginVisible = await this.loginButton.isVisible();
            return headingVisible && usernameVisible && passwordVisible && loginVisible;
        } catch {
            return false;
        }
    }

    /**
     * Clicks the Forgot Your Password link to navigate to password recovery.
     */
    async clickForgotPassword(): Promise<void> {
        try {
            await this.forgotPasswordLink.click();
        } catch (error) {
            throw new Error(`Failed to click Forgot Your Password link: ${error}`);
        }
    }

    /**
     * Clicks the Use Custom Domain link to switch to custom domain login.
     */
    async clickUseCustomDomain(): Promise<void> {
        try {
            await this.useCustomDomainLink.click();
        } catch (error) {
            throw new Error(`Failed to click Use Custom Domain link: ${error}`);
        }
    }
}