import {
  UniqueSelectionDispatcher
} from "./chunk-C6Y2VOIW.js";
import {
  ChangeDetectorRef,
  Directive,
  EventEmitter,
  Inject,
  InjectionToken,
  Input,
  NgModule,
  Optional,
  Output,
  SkipSelf,
  booleanAttribute,
  setClassMetadata,
  ɵɵInputTransformsFeature,
  ɵɵNgOnChangesFeature,
  ɵɵProvidersFeature,
  ɵɵdefineDirective,
  ɵɵdefineInjector,
  ɵɵdefineNgModule,
  ɵɵdirectiveInject
} from "./chunk-UHCMXLNU.js";
import {
  Subject,
  Subscription
} from "./chunk-F6TFW4TZ.js";

// node_modules/@angular/cdk/fesm2022/accordion.mjs
var nextId$1 = 0;
var CDK_ACCORDION = new InjectionToken("CdkAccordion");
var _CdkAccordion = class _CdkAccordion {
  constructor() {
    this._stateChanges = new Subject();
    this._openCloseAllActions = new Subject();
    this.id = `cdk-accordion-${nextId$1++}`;
    this.multi = false;
  }
  /** Opens all enabled accordion items in an accordion where multi is enabled. */
  openAll() {
    if (this.multi) {
      this._openCloseAllActions.next(true);
    }
  }
  /** Closes all enabled accordion items. */
  closeAll() {
    this._openCloseAllActions.next(false);
  }
  ngOnChanges(changes) {
    this._stateChanges.next(changes);
  }
  ngOnDestroy() {
    this._stateChanges.complete();
    this._openCloseAllActions.complete();
  }
};
_CdkAccordion.ɵfac = function CdkAccordion_Factory(t) {
  return new (t || _CdkAccordion)();
};
_CdkAccordion.ɵdir = ɵɵdefineDirective({
  type: _CdkAccordion,
  selectors: [["cdk-accordion"], ["", "cdkAccordion", ""]],
  inputs: {
    multi: [2, "multi", "multi", booleanAttribute]
  },
  exportAs: ["cdkAccordion"],
  standalone: true,
  features: [ɵɵProvidersFeature([{
    provide: CDK_ACCORDION,
    useExisting: _CdkAccordion
  }]), ɵɵInputTransformsFeature, ɵɵNgOnChangesFeature]
});
var CdkAccordion = _CdkAccordion;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(CdkAccordion, [{
    type: Directive,
    args: [{
      selector: "cdk-accordion, [cdkAccordion]",
      exportAs: "cdkAccordion",
      providers: [{
        provide: CDK_ACCORDION,
        useExisting: CdkAccordion
      }],
      standalone: true
    }]
  }], null, {
    multi: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }]
  });
})();
var nextId = 0;
var _CdkAccordionItem = class _CdkAccordionItem {
  /** Whether the AccordionItem is expanded. */
  get expanded() {
    return this._expanded;
  }
  set expanded(expanded) {
    if (this._expanded !== expanded) {
      this._expanded = expanded;
      this.expandedChange.emit(expanded);
      if (expanded) {
        this.opened.emit();
        const accordionId = this.accordion ? this.accordion.id : this.id;
        this._expansionDispatcher.notify(this.id, accordionId);
      } else {
        this.closed.emit();
      }
      this._changeDetectorRef.markForCheck();
    }
  }
  constructor(accordion, _changeDetectorRef, _expansionDispatcher) {
    this.accordion = accordion;
    this._changeDetectorRef = _changeDetectorRef;
    this._expansionDispatcher = _expansionDispatcher;
    this._openCloseAllSubscription = Subscription.EMPTY;
    this.closed = new EventEmitter();
    this.opened = new EventEmitter();
    this.destroyed = new EventEmitter();
    this.expandedChange = new EventEmitter();
    this.id = `cdk-accordion-child-${nextId++}`;
    this._expanded = false;
    this.disabled = false;
    this._removeUniqueSelectionListener = () => {
    };
    this._removeUniqueSelectionListener = _expansionDispatcher.listen((id, accordionId) => {
      if (this.accordion && !this.accordion.multi && this.accordion.id === accordionId && this.id !== id) {
        this.expanded = false;
      }
    });
    if (this.accordion) {
      this._openCloseAllSubscription = this._subscribeToOpenCloseAllActions();
    }
  }
  /** Emits an event for the accordion item being destroyed. */
  ngOnDestroy() {
    this.opened.complete();
    this.closed.complete();
    this.destroyed.emit();
    this.destroyed.complete();
    this._removeUniqueSelectionListener();
    this._openCloseAllSubscription.unsubscribe();
  }
  /** Toggles the expanded state of the accordion item. */
  toggle() {
    if (!this.disabled) {
      this.expanded = !this.expanded;
    }
  }
  /** Sets the expanded state of the accordion item to false. */
  close() {
    if (!this.disabled) {
      this.expanded = false;
    }
  }
  /** Sets the expanded state of the accordion item to true. */
  open() {
    if (!this.disabled) {
      this.expanded = true;
    }
  }
  _subscribeToOpenCloseAllActions() {
    return this.accordion._openCloseAllActions.subscribe((expanded) => {
      if (!this.disabled) {
        this.expanded = expanded;
      }
    });
  }
};
_CdkAccordionItem.ɵfac = function CdkAccordionItem_Factory(t) {
  return new (t || _CdkAccordionItem)(ɵɵdirectiveInject(CDK_ACCORDION, 12), ɵɵdirectiveInject(ChangeDetectorRef), ɵɵdirectiveInject(UniqueSelectionDispatcher));
};
_CdkAccordionItem.ɵdir = ɵɵdefineDirective({
  type: _CdkAccordionItem,
  selectors: [["cdk-accordion-item"], ["", "cdkAccordionItem", ""]],
  inputs: {
    expanded: [2, "expanded", "expanded", booleanAttribute],
    disabled: [2, "disabled", "disabled", booleanAttribute]
  },
  outputs: {
    closed: "closed",
    opened: "opened",
    destroyed: "destroyed",
    expandedChange: "expandedChange"
  },
  exportAs: ["cdkAccordionItem"],
  standalone: true,
  features: [ɵɵProvidersFeature([
    // Provide `CDK_ACCORDION` as undefined to prevent nested accordion items from
    // registering to the same accordion.
    {
      provide: CDK_ACCORDION,
      useValue: void 0
    }
  ]), ɵɵInputTransformsFeature]
});
var CdkAccordionItem = _CdkAccordionItem;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(CdkAccordionItem, [{
    type: Directive,
    args: [{
      selector: "cdk-accordion-item, [cdkAccordionItem]",
      exportAs: "cdkAccordionItem",
      providers: [
        // Provide `CDK_ACCORDION` as undefined to prevent nested accordion items from
        // registering to the same accordion.
        {
          provide: CDK_ACCORDION,
          useValue: void 0
        }
      ],
      standalone: true
    }]
  }], () => [{
    type: CdkAccordion,
    decorators: [{
      type: Optional
    }, {
      type: Inject,
      args: [CDK_ACCORDION]
    }, {
      type: SkipSelf
    }]
  }, {
    type: ChangeDetectorRef
  }, {
    type: UniqueSelectionDispatcher
  }], {
    closed: [{
      type: Output
    }],
    opened: [{
      type: Output
    }],
    destroyed: [{
      type: Output
    }],
    expandedChange: [{
      type: Output
    }],
    expanded: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }],
    disabled: [{
      type: Input,
      args: [{
        transform: booleanAttribute
      }]
    }]
  });
})();
var _CdkAccordionModule = class _CdkAccordionModule {
};
_CdkAccordionModule.ɵfac = function CdkAccordionModule_Factory(t) {
  return new (t || _CdkAccordionModule)();
};
_CdkAccordionModule.ɵmod = ɵɵdefineNgModule({
  type: _CdkAccordionModule,
  imports: [CdkAccordion, CdkAccordionItem],
  exports: [CdkAccordion, CdkAccordionItem]
});
_CdkAccordionModule.ɵinj = ɵɵdefineInjector({});
var CdkAccordionModule = _CdkAccordionModule;
(() => {
  (typeof ngDevMode === "undefined" || ngDevMode) && setClassMetadata(CdkAccordionModule, [{
    type: NgModule,
    args: [{
      imports: [CdkAccordion, CdkAccordionItem],
      exports: [CdkAccordion, CdkAccordionItem]
    }]
  }], null, null);
})();

export {
  CDK_ACCORDION,
  CdkAccordion,
  CdkAccordionItem,
  CdkAccordionModule
};
//# sourceMappingURL=chunk-7FJYHKTR.js.map
