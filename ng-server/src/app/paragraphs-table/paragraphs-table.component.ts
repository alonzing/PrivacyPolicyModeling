import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy} from "../../pp.service";
import {MatTableDataSource} from "@angular/material";
import {ThemeService} from "../../theme.service";

/**
 * Represents a filterable table of privacy policy paragraphs with three columns: 'Topic', 'Probability', and 'Text'.
 */
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

  /**
   * Used to filter paragraphs by filterValue.
   * @param filterValue The string that the table will be filtered by, case-insensitive.
   */
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

