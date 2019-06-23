import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy} from "../../pp.service";
import {MatTableDataSource} from "@angular/material";
import {ThemeService} from "../../theme.service";

@Component({
  selector: 'app-paragraphs-table',
  templateUrl: './paragraphs-table.component.html',
  styleUrls: ['./paragraphs-table.component.css']
})
export class ParagraphsTableComponent implements OnInit {
  displayedColumns: string[] = ['topic', 'probability', 'paragraph_text'];
  dataSource;
  isReady: boolean = false;

  constructor(public privacyPolicyService: PpService, public themeService: ThemeService) {
  }

  // static removeDuplicates(privacyPolicyData: PrivacyPolicy) {
  //   let currentParagraphIndex = -1;
  //   let modifiedParagraphs: ParagraphRow[] = [];
  //
  //   for (let paragraphRow of privacyPolicyData.paragraphs) {
  //     if (paragraphRow.index > currentParagraphIndex) {
  //       modifiedParagraphs.push(paragraphRow);
  //       currentParagraphIndex++;
  //     }
  //   }
  //   privacyPolicyData.paragraphs = modifiedParagraphs;
  // }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  ngOnInit() {
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicy: PrivacyPolicy) => {
      // ParagraphsTableComponent.removeDuplicates(privacyPolicy);
      this.dataSource = new MatTableDataSource(privacyPolicy.p);
      this.isReady = true;
    });

  }
}

