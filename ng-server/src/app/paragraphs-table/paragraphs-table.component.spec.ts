import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParagraphsTableComponent } from './paragraphs-table.component';

describe('ParagraphsTableComponent', () => {
  let component: ParagraphsTableComponent;
  let fixture: ComponentFixture<ParagraphsTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParagraphsTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParagraphsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
