import {Injectable, OnInit} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class ThemeService implements OnInit {
  isDarkMode: boolean = false;

  constructor(public cookieService: CookieService) {
    if (this.cookieService.check('isDarkMode')) {
      this.isDarkMode = this.cookieService.get('isDarkMode') === "true";
    }
  }

  toggleDarkMode() {
    this.isDarkMode = !this.isDarkMode;
    if (this.isDarkMode) {
      this.cookieService.set('isDarkMode', 'true');
    } else {
      this.cookieService.set('isDarkMode', 'false');

    }

  }

  ngOnInit(): void {

  }
}
