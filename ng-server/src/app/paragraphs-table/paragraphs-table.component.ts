import {Component, OnInit} from '@angular/core';
import {ParagraphRow, PpService, PrivacyPolicy} from "../../pp.service";
import {MatTableDataSource} from "@angular/material";
import {Observable} from "rxjs";

@Component({
  selector: 'app-paragraphs-table',
  templateUrl: './paragraphs-table.component.html',
  styleUrls: ['./paragraphs-table.component.css']
})
export class ParagraphsTableComponent implements OnInit {
  displayedColumns: string[] = ['index', 'topic', 'value'];
  dataSource;
  isReady: boolean = false;

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  static removeDuplicates(privacyPolicyData: PrivacyPolicy) {
    let currentParagraphIndex = -1;
    let modifiedParagraphs: ParagraphRow[] = [];

    for (let paragraphRow of privacyPolicyData.paragraphs) {
      if (paragraphRow.index > currentParagraphIndex) {
        modifiedParagraphs.push(paragraphRow);
        currentParagraphIndex++;
      }
    }
    privacyPolicyData.paragraphs = modifiedParagraphs;
  }

  constructor(public privacyPolicyService: PpService) {
  }

  ngOnInit() {
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicyObservable: Observable<PrivacyPolicy>) => {
      privacyPolicyObservable.subscribe((privacyPolicy: PrivacyPolicy) => {
        ParagraphsTableComponent.removeDuplicates(privacyPolicy);
        this.dataSource = new MatTableDataSource(privacyPolicy.paragraphs);
        this.isReady = true;
      })
    });

  }

}

