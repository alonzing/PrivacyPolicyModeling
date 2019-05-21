import {Component, OnInit} from '@angular/core';
import {FormControl} from '@angular/forms';
import {PpService} from "../../pp.service";

@Component({
  selector: 'app-pp-url-search',
  templateUrl: './pp-url-search.component.html',
  styleUrls: ['./pp-url-search.component.css']
})
export class PpUrlSearchComponent implements OnInit {
  urlFormControl = new FormControl('');

  constructor(private privacyPolicyService: PpService) {
  }

  getPrivacyPolicyData(){
    console.log("Submitted " + this.urlFormControl.value);
    this.privacyPolicyService.getPrivacyPolicy(this.urlFormControl.value).subscribe();
  }
  ngOnInit() {}


}
