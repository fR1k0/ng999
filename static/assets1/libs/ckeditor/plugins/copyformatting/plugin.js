/*
 Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
*/
(function () {
  function k(a, b, e, d) {
    var c = new CKEDITOR.dom.walker(a);
    if (
      (a =
        a.startContainer.getAscendant(b, !0) ||
        a.endContainer.getAscendant(b, !0))
    )
      if ((e(a), d)) return;
    for (; (a = c.next()); )
      if ((a = a.getAscendant(b, !0))) if ((e(a), d)) break;
  }
  function u(a, b) {
    var e = { ul: "ol", ol: "ul" };
    return (
      -1 !==
      l(b, function (b) {
        return b.element === a || b.element === e[a];
      })
    );
  }
  function q(a) {
    this.styles = null;
    this.sticky = !1;
    this.editor = a;
    this.filter = new CKEDITOR.filter(a, a.config.copyFormatting_allowRules);
    !0 === a.config.copyFormatting_allowRules && (this.filter.disabled = !0);
    a.config.copyFormatting_disallowRules &&
      this.filter.disallow(a.config.copyFormatting_disallowRules);
  }
  var l = CKEDITOR.tools.indexOf,
    r = CKEDITOR.tools.getMouseButton,
    t = !1;
  CKEDITOR.plugins.add("copyformatting", {
    lang: "az,de,en,it,ja,nb,nl,oc,pl,pt-br,ru,sv,tr,zh,zh-cn",
    icons: "copyformatting",
    hidpi: !0,
    init: function (a) {
      var b = CKEDITOR.plugins.copyformatting;
      b._addScreenReaderContainer();
      t ||
        (CKEDITOR.document.appendStyleSheet(
          this.path + "styles/copyformatting.css"
        ),
        (t = !0));
      a.addContentsCss &&
        a.addContentsCss(this.path + "styles/copyformatting.css");
      a.copyFormatting = new b.state(a);
      a.addCommand("copyFormatting", b.commands.copyFormatting);
      a.addCommand("applyFormatting", b.commands.applyFormatting);
      a.ui.addButton("CopyFormatting", {
        label: a.lang.copyformatting.label,
        command: "copyFormatting",
        toolbar: "cleanup,0",
      });
      a.on("contentDom", function () {
        var b = a.getCommand("copyFormatting"),
          d = a.editable(),
          c = d.isInline() ? d : a.document,
          f = a.ui.get("CopyFormatting");
        d.attachListener(c, "mouseup", function (d) {
          r(d) === CKEDITOR.MOUSE_BUTTON_LEFT &&
            b.state === CKEDITOR.TRISTATE_ON &&
            a.execCommand("applyFormatting");
        });
        d.attachListener(CKEDITOR.document, "mouseup", function (c) {
          r(c) !== CKEDITOR.MOUSE_BUTTON_LEFT ||
            b.state !== CKEDITOR.TRISTATE_ON ||
            d.contains(c.data.getTarget()) ||
            a.execCommand("copyFormatting");
        });
        f &&
          ((c = CKEDITOR.document.getById(f._.id)),
          d.attachListener(c, "dblclick", function () {
            a.execCommand("copyFormatting", { sticky: !0 });
          }),
          d.attachListener(c, "mouseup", function (a) {
            a.data.stopPropagation();
          }));
      });
      a.config.copyFormatting_keystrokeCopy &&
        a.setKeystroke(a.config.copyFormatting_keystrokeCopy, "copyFormatting");
      a.on("key", function (b) {
        var d = a.getCommand("copyFormatting");
        b = b.data.domEvent;
        b.getKeystroke &&
          27 === b.getKeystroke() &&
          d.state === CKEDITOR.TRISTATE_ON &&
          a.execCommand("copyFormatting");
      });
      a.copyFormatting.on("extractFormatting", function (e) {
        var d = e.data.element;
        if (d.contains(a.editable()) || d.equals(a.editable()))
          return e.cancel();
        d = b._convertElementToStyleDef(d);
        if (!a.copyFormatting.filter.check(new CKEDITOR.style(d), !0, !0))
          return e.cancel();
        e.data.styleDef = d;
      });
      a.copyFormatting.on("applyFormatting", function (e) {
        if (!e.data.preventFormatStripping) {
          var d = e.data.range,
            c = b._extractStylesFromRange(a, d),
            f = b._determineContext(d),
            g,
            h;
          if (a.copyFormatting._isContextAllowed(f))
            for (h = 0; h < c.length; h++)
              (f = c[h]),
                (g = d.createBookmark()),
                -1 === l(b.preservedElements, f.element)
                  ? CKEDITOR.env.webkit && !CKEDITOR.env.chrome
                    ? c[h].removeFromRange(e.data.range, e.editor)
                    : c[h].remove(e.editor)
                  : u(f.element, e.data.styles) &&
                    b._removeStylesFromElementInRange(d, f.element),
                d.moveToBookmark(g);
        }
      });
      a.copyFormatting.on(
        "applyFormatting",
        function (b) {
          var d = CKEDITOR.plugins.copyformatting,
            c = d._determineContext(b.data.range);
          "list" === c && a.copyFormatting._isContextAllowed("list")
            ? d._applyStylesToListContext(b.editor, b.data.range, b.data.styles)
            : "table" === c && a.copyFormatting._isContextAllowed("table")
            ? d._applyStylesToTableContext(
                b.editor,
                b.data.range,
                b.data.styles
              )
            : a.copyFormatting._isContextAllowed("text") &&
              d._applyStylesToTextContext(
                b.editor,
                b.data.range,
                b.data.styles
              );
        },
        null,
        null,
        999
      );
    },
  });
  q.prototype._isContextAllowed = function (a) {
    var b = this.editor.config.copyFormatting_allowedContexts;
    return !0 === b || -1 !== l(b, a);
  };
  CKEDITOR.event.implementOn(q.prototype);
  CKEDITOR.plugins.copyformatting = {
    state: q,
    inlineBoundary: "h1 h2 h3 h4 h5 h6 p div".split(" "),
    excludedAttributes: ["id", "style", "href", "data-cke-saved-href", "dir"],
    elementsForInlineTransform: ["li"],
    excludedElementsFromInlineTransform: [
      "table",
      "thead",
      "tbody",
      "ul",
      "ol",
    ],
    excludedAttributesFromInlineTransform: ["value", "type"],
    preservedElements: "ul ol li td th tr thead tbody table".split(" "),
    breakOnElements: ["ul", "ol", "table"],
    _initialKeystrokePasteCommand: null,
    commands: {
      copyFormatting: {
        exec: function (a, b) {
          var e = CKEDITOR.plugins.copyformatting,
            d = a.copyFormatting,
            c = b ? "keystrokeHandler" == b.from : !1,
            f = b ? b.sticky || c : !1,
            g = e._getCursorContainer(a),
            h = CKEDITOR.document.getDocumentElement();
          if (this.state === CKEDITOR.TRISTATE_ON)
            return (
              (d.styles = null),
              (d.sticky = !1),
              g.removeClass("cke_copyformatting_active"),
              h.removeClass("cke_copyformatting_disabled"),
              h.removeClass("cke_copyformatting_tableresize_cursor"),
              e._putScreenReaderMessage(a, "canceled"),
              e._detachPasteKeystrokeHandler(a),
              this.setState(CKEDITOR.TRISTATE_OFF)
            );
          d.styles = e._extractStylesFromElement(
            a,
            a.elementPath().lastElement
          );
          this.setState(CKEDITOR.TRISTATE_ON);
          c ||
            (g.addClass("cke_copyformatting_active"),
            h.addClass("cke_copyformatting_tableresize_cursor"),
            a.config.copyFormatting_outerCursor &&
              h.addClass("cke_copyformatting_disabled"));
          d.sticky = f;
          e._putScreenReaderMessage(a, "copied");
          e._attachPasteKeystrokeHandler(a);
        },
      },
      applyFormatting: {
        editorFocus: CKEDITOR.env.ie && !CKEDITOR.env.edge ? !1 : !0,
        exec: function (a, b) {
          var e = a.getCommand("copyFormatting"),
            d = b ? "keystrokeHandler" == b.from : !1,
            c = CKEDITOR.plugins.copyformatting,
            f = a.copyFormatting,
            g = c._getCursorContainer(a),
            h = CKEDITOR.document.getDocumentElement();
          if (d && !f.styles)
            return (
              c._putScreenReaderMessage(a, "failed"),
              c._detachPasteKeystrokeHandler(a),
              !1
            );
          d = c._applyFormat(a, f.styles);
          f.sticky ||
            ((f.styles = null),
            g.removeClass("cke_copyformatting_active"),
            h.removeClass("cke_copyformatting_disabled"),
            h.removeClass("cke_copyformatting_tableresize_cursor"),
            e.setState(CKEDITOR.TRISTATE_OFF),
            c._detachPasteKeystrokeHandler(a));
          c._putScreenReaderMessage(a, d ? "applied" : "canceled");
        },
      },
    },
    _getCursorContainer: function (a) {
      return a.elementMode === CKEDITOR.ELEMENT_MODE_INLINE
        ? a.editable()
        : a.editable().getParent();
    },
    _convertElementToStyleDef: function (a) {
      var b = CKEDITOR.tools,
        e = a.getAttributes(CKEDITOR.plugins.copyformatting.excludedAttributes),
        b = b.parseCssText(a.getAttribute("style"), !0, !0);
      return {
        element: a.getName(),
        type: CKEDITOR.STYLE_INLINE,
        attributes: e,
        styles: b,
      };
    },
    _extractStylesFromElement: function (a, b) {
      var e = {},
        d = [];
      do
        if (
          b.type === CKEDITOR.NODE_ELEMENT &&
          !b.hasAttribute("data-cke-bookmark") &&
          ((e.element = b),
          a.copyFormatting.fire("extractFormatting", e, a) &&
            e.styleDef &&
            d.push(new CKEDITOR.style(e.styleDef)),
          b.getName &&
            -1 !==
              l(CKEDITOR.plugins.copyformatting.breakOnElements, b.getName()))
        )
          break;
      while ((b = b.getParent()) && b.type === CKEDITOR.NODE_ELEMENT);
      return d;
    },
    _extractStylesFromRange: function (a, b) {
      for (var e = [], d = new CKEDITOR.dom.walker(b), c; (c = d.next()); )
        e = e.concat(
          CKEDITOR.plugins.copyformatting._extractStylesFromElement(a, c)
        );
      return e;
    },
    _removeStylesFromElementInRange: function (a, b) {
      for (
        var e = -1 !== l(["ol", "ul", "table"], b),
          d = new CKEDITOR.dom.walker(a),
          c;
        (c = d.next());

      )
        if ((c = c.getAscendant(b, !0)))
          if ((c.removeAttributes(c.getAttributes()), e)) break;
    },
    _getSelectedWordOffset: function (a) {
      function b(a, b) {
        return a[b ? "getPrevious" : "getNext"](function (a) {
          return a.type !== CKEDITOR.NODE_COMMENT;
        });
      }
      function e(a) {
        return a.type == CKEDITOR.NODE_ELEMENT
          ? ((a = a.getHtml().replace(/<span.*?>&nbsp;<\/span>/g, "")),
            a.replace(/<.*?>/g, ""))
          : a.getText();
      }
      function d(a, c) {
        var f = a,
          g = /\s/g,
          h = "p br ol ul li td th div caption body".split(" "),
          m = !1,
          k = !1,
          p,
          n;
        do {
          for (p = b(f, c); !p && f.getParent(); ) {
            f = f.getParent();
            if (-1 !== l(h, f.getName())) {
              k = m = !0;
              break;
            }
            p = b(f, c);
          }
          if (p && p.getName && -1 !== l(h, p.getName())) {
            m = !0;
            break;
          }
          f = p;
        } while (
          f &&
          f.getStyle &&
          ("none" == f.getStyle("display") || !f.getText())
        );
        for (f || (f = a); f.type !== CKEDITOR.NODE_TEXT; )
          f = !m || c || k ? f.getChild(0) : f.getChild(f.getChildCount() - 1);
        for (h = e(f); null != (k = g.exec(h)) && ((n = k.index), c); );
        if ("number" !== typeof n && !m) return d(f, c);
        if (m)
          c
            ? (n = 0)
            : ((g = /([\.\b]*$)/), (n = (k = g.exec(h)) ? k.index : h.length));
        else if (c && ((n += 1), n > h.length)) return d(f);
        return { node: f, offset: n };
      }
      var c = /\b\w+\b/gi,
        f,
        g,
        h,
        m,
        k;
      h = m = k = a.startContainer;
      for (f = e(h); null != (g = c.exec(f)); )
        if (g.index + g[0].length >= a.startOffset)
          return (
            (a = g.index),
            (c = g.index + g[0].length),
            0 === g.index && ((g = d(h, !0)), (m = g.node), (a = g.offset)),
            c >= f.length && ((f = d(h)), (k = f.node), (c = f.offset)),
            { startNode: m, startOffset: a, endNode: k, endOffset: c }
          );
      return null;
    },
    _filterStyles: function (a) {
      var b = CKEDITOR.tools.isEmpty,
        e = [],
        d,
        c;
      for (c = 0; c < a.length; c++)
        (d = a[c]._.definition),
          -1 !==
            CKEDITOR.tools.indexOf(
              CKEDITOR.plugins.copyformatting.inlineBoundary,
              d.element
            ) && (d.element = a[c].element = "span"),
          ("span" === d.element && b(d.attributes) && b(d.styles)) ||
            e.push(a[c]);
      return e;
    },
    _determineContext: function (a) {
      function b(b) {
        var d = new CKEDITOR.dom.walker(a),
          c;
        if (
          a.startContainer.getAscendant(b, !0) ||
          a.endContainer.getAscendant(b, !0)
        )
          return !0;
        for (; (c = d.next()); ) if (c.getAscendant(b, !0)) return !0;
      }
      return b({ ul: 1, ol: 1 }) ? "list" : b("table") ? "table" : "text";
    },
    _applyStylesToTextContext: function (a, b, e) {
      var d = CKEDITOR.plugins.copyformatting,
        c = d.excludedAttributesFromInlineTransform,
        f,
        g;
      CKEDITOR.env.webkit &&
        !CKEDITOR.env.chrome &&
        a.getSelection().selectRanges([b]);
      for (f = 0; f < e.length; f++)
        if (
          ((b = e[f]),
          -1 === l(d.excludedElementsFromInlineTransform, b.element))
        ) {
          if (-1 !== l(d.elementsForInlineTransform, b.element))
            for (
              b.element = b._.definition.element = "span", g = 0;
              g < c.length;
              g++
            )
              b._.definition.attributes[c[g]] &&
                delete b._.definition.attributes[c[g]];
          b.apply(a);
        }
    },
    _applyStylesToListContext: function (a, b, e) {
      var d, c, f;
      for (f = 0; f < e.length; f++)
        (d = e[f]),
          (c = b.createBookmark()),
          "ol" === d.element || "ul" === d.element
            ? k(
                b,
                { ul: 1, ol: 1 },
                function (a) {
                  var b = d;
                  a.getName() !== b.element && a.renameNode(b.element);
                  b.applyToObject(a);
                },
                !0
              )
            : "li" === d.element
            ? k(b, "li", function (a) {
                d.applyToObject(a);
              })
            : CKEDITOR.plugins.copyformatting._applyStylesToTextContext(a, b, [
                d,
              ]),
          b.moveToBookmark(c);
    },
    _applyStylesToTableContext: function (a, b, e) {
      function d(a, b) {
        a.getName() !== b.element &&
          ((b = b.getDefinition()),
          (b.element = a.getName()),
          (b = new CKEDITOR.style(b)));
        b.applyToObject(a);
      }
      var c, f, g;
      for (g = 0; g < e.length; g++)
        (c = e[g]),
          (f = b.createBookmark()),
          -1 !== l(["table", "tr"], c.element)
            ? k(b, c.element, function (a) {
                c.applyToObject(a);
              })
            : -1 !== l(["td", "th"], c.element)
            ? k(b, { td: 1, th: 1 }, function (a) {
                d(a, c);
              })
            : -1 !== l(["thead", "tbody"], c.element)
            ? k(b, { thead: 1, tbody: 1 }, function (a) {
                d(a, c);
              })
            : CKEDITOR.plugins.copyformatting._applyStylesToTextContext(a, b, [
                c,
              ]),
          b.moveToBookmark(f);
    },
    _applyFormat: function (a, b) {
      var e = a.getSelection().getRanges()[0],
        d = CKEDITOR.plugins.copyformatting,
        c,
        f;
      if (!e) return !1;
      if (e.collapsed) {
        f = a.getSelection().createBookmarks();
        if (!(c = d._getSelectedWordOffset(e))) return;
        e = a.createRange();
        e.setStart(c.startNode, c.startOffset);
        e.setEnd(c.endNode, c.endOffset);
        e.select();
      }
      b = d._filterStyles(b);
      if (
        !a.copyFormatting.fire(
          "applyFormatting",
          { styles: b, range: e, preventFormatStripping: !1 },
          a
        )
      )
        return !1;
      f && a.getSelection().selectBookmarks(f);
      return !0;
    },
    _putScreenReaderMessage: function (a, b) {
      var e = this._getScreenReaderContainer();
      e && e.setText(a.lang.copyformatting.notification[b]);
    },
    _addScreenReaderContainer: function () {
      if (this._getScreenReaderContainer())
        return this._getScreenReaderContainer();
      if (!CKEDITOR.env.ie6Compat && !CKEDITOR.env.ie7Compat)
        return CKEDITOR.document
          .getBody()
          .append(
            CKEDITOR.dom.element.createFromHtml(
              '\x3cdiv class\x3d"cke_screen_reader_only cke_copyformatting_notification"\x3e\x3cdiv aria-live\x3d"polite"\x3e\x3c/div\x3e\x3c/div\x3e'
            )
          )
          .getChild(0);
    },
    _getScreenReaderContainer: function () {
      if (!CKEDITOR.env.ie6Compat && !CKEDITOR.env.ie7Compat)
        return CKEDITOR.document
          .getBody()
          .findOne(".cke_copyformatting_notification div[aria-live]");
    },
    _attachPasteKeystrokeHandler: function (a) {
      var b = a.config.copyFormatting_keystrokePaste;
      b &&
        ((this._initialKeystrokePasteCommand =
          a.keystrokeHandler.keystrokes[b]),
        a.setKeystroke(b, "applyFormatting"));
    },
    _detachPasteKeystrokeHandler: function (a) {
      var b = a.config.copyFormatting_keystrokePaste;
      b && a.setKeystroke(b, this._initialKeystrokePasteCommand || !1);
    },
  };
  CKEDITOR.config.copyFormatting_outerCursor = !0;
  CKEDITOR.config.copyFormatting_allowRules =
    "b s u i em strong span p div td th ol ul li(*)[*]{*}";
  CKEDITOR.config.copyFormatting_disallowRules =
    "*[data-cke-widget*,data-widget*,data-cke-realelement](cke_widget*)";
  CKEDITOR.config.copyFormatting_allowedContexts = !0;
  CKEDITOR.config.copyFormatting_keystrokeCopy =
    CKEDITOR.CTRL + CKEDITOR.SHIFT + 67;
  CKEDITOR.config.copyFormatting_keystrokePaste =
    CKEDITOR.CTRL + CKEDITOR.SHIFT + 86;
})();
