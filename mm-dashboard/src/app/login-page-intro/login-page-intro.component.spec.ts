import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginPageIntroComponent } from './login-page-intro.component';

describe('LoginPageIntroComponent', () => {
  let component: LoginPageIntroComponent;
  let fixture: ComponentFixture<LoginPageIntroComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginPageIntroComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginPageIntroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
