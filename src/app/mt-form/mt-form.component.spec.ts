import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MTFormComponent } from './mt-form.component';

describe('MTFormComponent', () => {
  let component: MTFormComponent;
  let fixture: ComponentFixture<MTFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MTFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MTFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
