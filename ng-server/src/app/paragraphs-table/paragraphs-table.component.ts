import { Component, OnInit } from '@angular/core';
import {PpService} from "../../pp.service";

@Component({
  selector: 'app-paragraphs-table',
  templateUrl: './paragraphs-table.component.html',
  styleUrls: ['./paragraphs-table.component.css']
})
export class ParagraphsTableComponent implements OnInit {

  constructor(public privacyPolicyService: PpService) { }

  ngOnInit() {
  }

}
