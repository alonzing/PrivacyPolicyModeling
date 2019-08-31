import {Component, OnInit} from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import {PpService, PrivacyPolicy} from "../../pp.service";
import {MatButtonModule} from '@angular/material/button';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {ThemeService} from "../../theme.service";
import {MatSelectModule} from "@angular/material";

/**
 * Represents a search box where the user can submit a privacy policy URL and a category.
 */
@Component({
  selector: 'app-pp-url-search',
  templateUrl: './pp-url-search.component.html',
  styleUrls: ['./pp-url-search.component.css']
})

export class PpUrlSearchComponent implements OnInit {
  privacyPolicyUrl = new FormControl('', [
    Validators.required,
  ]);

  privacyPolicyCategory = new FormControl('', [
    Validators.required,
  ]);
  categories: string[];

  constructor(public privacyPolicyService: PpService, public themeService: ThemeService) {
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicy: PrivacyPolicy) => {
      this.privacyPolicyService.progressBar = false;
      if (privacyPolicy == null) {
        return
      }
    });
  }

  /**
   * Gets the privacy policy data.
   */
  getPrivacyPolicyData() {
    this.privacyPolicyService.progressBar = true;
    this.privacyPolicyService.getPrivacyPolicy(this.privacyPolicyUrl.value, this.privacyPolicyCategory.value).subscribe();
    console.log("Submitted " + this.privacyPolicyUrl.value);
  }


  ngOnInit() {
    this.privacyPolicyService.getCategories().subscribe((categories: string[]) => {
      this.categories = categories;
    });
  }
}
