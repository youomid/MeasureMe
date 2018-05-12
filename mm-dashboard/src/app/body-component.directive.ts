import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[appBodyComponent]'
})
export class BodyComponentDirective {

	constructor(public viewContainerRef: ViewContainerRef) { }

}
