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
        gui_hooks.editor_did_load_note.append(self.editor_note_hook)
        gui_hooks.editor_did_fire_typing_timer.append(self.onedit_hook)

    def editor_init_hook(self, ed: editor.Editor):
        self.webview = AnkiWebView(title="editor_preview")
        # This is taken out of clayout.py
        self.webview.stdHtml(
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
        self.webview.setMaximumHeight = 400
        layout.addWidget(self.webview, 1)

    def editor_note_hook(self, editor):
        self.onedit_hook(editor.note)


    def _obtainCardText(self, note):
        c = note.ephemeral_card()
        a = mw.prepare_card_text_for_display(c.answer())
        a = gui_hooks.card_will_show(a, c, "clayoutAnswer")
        bodyclass = theme_manager.body_classes_for_card_ord(c.ord, mw.pm.night_mode())

        return f"_showAnswer({json.dumps(a)},'{bodyclass}');"

    def onedit_hook(self, note):
        self.webview.eval(self._obtainCardText(note))


eprev = EditorPreview()
