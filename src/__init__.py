from aqt.qt import *
import json
from anki import hooks
from aqt import editor
from aqt.webview import AnkiWebView
from aqt.theme import theme_manager
from aqt import gui_hooks
from aqt import mw

class EditorPreview(object):

    def __init__(self):
        gui_hooks.editor_did_init.append(self.editor_init_hook)

    def editor_init_hook(self, ed: editor.Editor):
        ed.webview = AnkiWebView(title="editor_preview")
        # This is taken out of clayout.py
        ed.webview.stdHtml(
            ed.mw.reviewer.revHtml(),
            css=["css/reviewer.css"],
            js=[
                "js/mathjax.js",
                "js/vendor/mathjax/tex-chtml.js",
                "js/reviewer.js",
            ],
            context=ed,
        )
        layout = ed.outerLayout
        # very arbitrary max size
        # otherwise the browse window is not usable
        ed.webview.setMaximumHeight = 400
        layout.addWidget(ed.webview, 1)
        gui_hooks.editor_did_fire_typing_timer.append(lambda o: self.onedit_hook(ed, o))
        gui_hooks.editor_did_load_note.append(lambda o: None if o != ed else self.editor_note_hook(o))

    def editor_note_hook(self, editor):
        self.onedit_hook(editor, editor.note)


    def _obtainCardText(self, note):
        c = note.ephemeral_card()
        a = mw.prepare_card_text_for_display(c.answer())
        a = gui_hooks.card_will_show(a, c, "clayoutAnswer")
        bodyclass = theme_manager.body_classes_for_card_ord(c.ord, mw.pm.night_mode())

        return f"_showAnswer({json.dumps(a)},'{bodyclass}');"

    def onedit_hook(self, editor, origin):
        if editor.note == origin:
            editor.webview.eval(self._obtainCardText(editor.note))


eprev = EditorPreview()
