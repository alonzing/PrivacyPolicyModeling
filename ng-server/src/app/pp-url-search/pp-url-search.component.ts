import {Component, NgModule, OnInit} from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import {PpService, PrivacyPolicy} from "../../pp.service";
import {MatButtonModule} from '@angular/material/button';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {ThemeService} from "../../theme.service";

@Component({
  selector: 'app-pp-url-search',
  templateUrl: './pp-url-search.component.html',
  styleUrls: ['./pp-url-search.component.css']
})

@NgModule({
  imports: [MatButtonModule, BrowserAnimationsModule, MatInputModule, MatFormFieldModule]
})

export class PpUrlSearchComponent implements OnInit {

  pPUrl = new FormControl('', [
    Validators.required,
  ]);

  constructor(public privacyPolicyService: PpService, public themeService: ThemeService) {
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicy: PrivacyPolicy) => {
      this.privacyPolicyService.progressBar = false;
      if (privacyPolicy == null) {
        return
      }
    });
  }

  getPrivacyPolicyData() {
    this.privacyPolicyService.progressBar = true;
    this.privacyPolicyService.getPrivacyPolicy(this.pPUrl.value).subscribe();
    console.log("Submitted " + this.pPUrl.value);
  }


  ngOnInit() {
  }


}
