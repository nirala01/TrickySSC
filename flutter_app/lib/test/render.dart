// Turns question, option and solution text into widgets, following the website's
// formatQText / renderContent: [IMG]…[/IMG] figures, [BR] line breaks, **bold**,
// *italic*, pipe tables, and LaTeX between \( \) or \[ \].
import 'package:flutter/material.dart';
import 'package:flutter_math_fork/flutter_math.dart';
import 'package:flutter_widget_from_html_core/flutter_widget_from_html_core.dart';

/// imgbb figures load through the same image CDN the website uses.
String figureUrl(String u) {
  if (RegExp(r'^https?://(i\.)?ibb\.co/', caseSensitive: false).hasMatch(u)) {
    return 'https://wsrv.nl/?url=${Uri.encodeComponent(u.replaceFirst(RegExp(r'^https?://', caseSensitive: false), ''))}&w=1000&we';
  }
  return u;
}

String stripFigRef(String t) =>
    RegExp(r'^\s*\(\s*(?:figure|आकृति|चित्र)\s*[1-4]\s*\)\s*$', caseSensitive: false).hasMatch(t) ? '' : t;

String _esc(String s) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

/// LaTeX pieces become <tex> elements (rendered by flutter_math_fork).
String _texify(String s) {
  s = s.replaceAllMapped(RegExp(r'\\\[(.+?)\\\]', dotAll: true), (m) => '<tex data-d="1">${_esc(m[1]!)}</tex>');
  s = s.replaceAllMapped(RegExp(r'\\\((.+?)\\\)', dotAll: true), (m) => '<tex>${_esc(m[1]!)}</tex>');
  return s;
}

String _brBold(String text) {
  var s = text.split('[BR]').join('<br>');
  s = s.replaceAllMapped(RegExp(r'\*\*(.+?)\*\*'), (m) => '<b>${m[1]}</b>');
  s = s.replaceAllMapped(RegExp(r'(^|[^*])\*([^*\n]+?)\*(?!\*)'), (m) => '${m[1]}<i>${m[2]}</i>');
  return s;
}

String _resolveImg(String t) => t.replaceAllMapped(RegExp(r'\[IMG\](.*?)\[/IMG\]'), (m) => '<img src="${figureUrl(m[1]!.trim())}">');

List<String> _lines(String raw) => raw.split(RegExp(r'\[BR\]|<br\s*/?>|\n', caseSensitive: false)).map((s) => s.trim()).toList();

bool _isPipeRow(String s) => '|'.allMatches(s).length >= 2;

String? _table(List<String> parts) {
  final rows = <String>[], caption = <String>[], after = <String>[];
  var inTable = false, past = false;
  for (final seg in parts) {
    if (seg.isEmpty) {
      if (inTable) {
        past = true;
        inTable = false;
      }
      continue;
    }
    if (_isPipeRow(seg)) {
      if (RegExp(r'^\|[\s\-|:]+\|$').hasMatch(seg)) continue;
      inTable = true;
      past = false;
      rows.add(seg);
    } else if (past || (rows.isNotEmpty && !inTable)) {
      after.add(seg);
    } else {
      caption.add(seg);
    }
  }
  if (rows.isEmpty) return null;
  List<String> cells(String r) => r.split('|').map((c) => c.trim()).where((c) => c.isNotEmpty).toList();
  final b = StringBuffer();
  if (caption.isNotEmpty) b.write('<p>${caption.join(' ')}</p>');
  b.write('<table border="1" cellpadding="6"><tr>');
  for (final h in cells(rows.first)) {
    b.write('<th>$h</th>');
  }
  b.write('</tr>');
  for (final r in rows.skip(1)) {
    b.write('<tr>');
    for (final c in cells(r)) {
      b.write('<td>$c</td>');
    }
    b.write('</tr>');
  }
  b.write('</table>');
  if (after.isNotEmpty) b.write('<p>${after.join('<br>')}</p>');
  return b.toString();
}

/// Question text → HTML (website: formatQText).
String questionHtml(String raw) {
  raw = raw.replaceFirst(RegExp(r'^\s*\[FIGURE-BASED\]\s*', caseSensitive: false), '');
  if (raw.isEmpty) return '';
  raw = _resolveImg(raw);
  String out;
  if (raw.contains('||')) {
    final halves = raw.split('||');
    final instr = halves.first.trim();
    final body = halves.skip(1).join('').trim();
    final t = _lines(body).any(_isPipeRow) ? _table(_lines(body)) : null;
    out = '<p><i>${_brBold(instr)}</i></p>${t ?? '<p>${_brBold(body)}</p>'}';
  } else {
    final t = _lines(raw).any(_isPipeRow) ? _table(_lines(raw)) : null;
    out = t ?? _brBold(raw);
  }
  return _texify(out);
}

/// Option and solution text → HTML (website: [BR] handling + renderContent).
String contentHtml(String raw) {
  if (raw.isEmpty) return '';
  var s = _resolveImg(raw.split('[BR]').join('<br>'));
  final hasTags = RegExp(r'<[a-z]', caseSensitive: false).hasMatch(s);
  if (!hasTags) s = s.replaceAll('\n', '<br>');
  s = s.replaceAllMapped(RegExp(r'\*\*(.+?)\*\*'), (m) => '<b>${m[1]}</b>');
  return _texify(s);
}

class Rich extends StatelessWidget {
  final String html;
  final double size;
  final Color color;
  final FontWeight weight;
  const Rich(this.html, {super.key, this.size = 16, this.color = const Color(0xFF0F172A), this.weight = FontWeight.w500});

  @override
  Widget build(BuildContext context) {
    return HtmlWidget(
      html,
      textStyle: TextStyle(fontSize: size, color: color, height: 1.45, fontWeight: weight),
      customStylesBuilder: (e) {
        if (e.localName == 'th') return {'background-color': '#F1F5F9', 'font-weight': 'bold'};
        if (e.localName == 'table') return {'border-collapse': 'collapse'};
        return null;
      },
      customWidgetBuilder: (e) {
        if (e.localName == 'tex') {
          final display = e.attributes['data-d'] == '1';
          final w = Math.tex(
            e.text,
            mathStyle: display ? MathStyle.display : MathStyle.text,
            textStyle: TextStyle(fontSize: size, color: color),
            onErrorFallback: (err) => Text(e.text, style: TextStyle(fontSize: size, color: color)),
          );
          return display ? Center(child: Padding(padding: const EdgeInsets.symmetric(vertical: 4), child: w)) : InlineCustomWidget(child: w);
        }
        if (e.localName == 'img') {
          final src = e.attributes['src'] ?? '';
          if (src.isEmpty) return null;
          return Figure(src);
        }
        return null;
      },
    );
  }
}

/// A figure that shows a loader, and a "Tap to retry" box if it fails.
class Figure extends StatefulWidget {
  final String url;
  final double maxHeight;
  final bool tapZoom;
  const Figure(this.url, {super.key, this.maxHeight = 320, this.tapZoom = true});

  @override
  State<Figure> createState() => _FigureState();
}

void openFigure(BuildContext context, String url) {
  Navigator.of(context).push(PageRouteBuilder(
    opaque: false,
    barrierColor: Colors.black,
    pageBuilder: (c, _, __) => _FigureViewer(figureUrl(url)),
  ));
}

class _FigureViewer extends StatelessWidget {
  final String src;
  const _FigureViewer(this.src);
  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: Colors.black,
        body: SafeArea(
          child: Stack(children: [
            Positioned.fill(
              child: InteractiveViewer(
                minScale: 1,
                maxScale: 6,
                child: Center(
                  child: Container(
                    color: Colors.white,
                    child: Image.network(src, fit: BoxFit.contain, width: double.infinity),
                  ),
                ),
              ),
            ),
            Positioned(
              top: 8,
              right: 8,
              child: IconButton.filled(
                style: IconButton.styleFrom(backgroundColor: Colors.white24),
                onPressed: () => Navigator.of(context).pop(),
                icon: const Icon(Icons.close, color: Colors.white),
              ),
            ),
            const Positioned(
              bottom: 12,
              left: 0,
              right: 0,
              child: Text('Pinch to zoom', textAlign: TextAlign.center, style: TextStyle(color: Colors.white70, fontSize: 12)),
            ),
          ]),
        ),
      );
}

class _FigureState extends State<Figure> {
  int _try = 0;

  Widget _loader() => Container(
        height: 90,
        alignment: Alignment.center,
        decoration: BoxDecoration(color: const Color(0xFFF8FAFC), borderRadius: BorderRadius.circular(10)),
        child: const Row(mainAxisSize: MainAxisSize.min, children: [
          SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2.5)),
          SizedBox(width: 10),
          Text('Loading figure…', style: TextStyle(color: Color(0xFF64748B), fontSize: 13)),
        ]),
      );

  @override
  Widget build(BuildContext context) {
    final u = figureUrl(widget.url);
    final src = _try == 0 ? u : '$u${u.contains('?') ? '&' : '?'}_r=$_try';
    bool ok = false;
    final img = Image.network(
      src,
      key: ValueKey(src),
      fit: BoxFit.contain,
      frameBuilder: (c, child, frame, sync) {
        if (sync || frame != null) {
          ok = true;
          return child;
        }
        return _loader();
      },
      loadingBuilder: (c, child, p) => p == null ? child : _loader(),
      errorBuilder: (c, e, s) => InkWell(
        onTap: () => setState(() => _try++),
        child: Container(
          height: 64,
          alignment: Alignment.center,
          decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(10)),
          child: const Text('Figure could not load · Tap to retry', style: TextStyle(color: Color(0xFF475569), fontSize: 13)),
        ),
      ),
    );
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: ConstrainedBox(
        constraints: BoxConstraints(maxHeight: widget.maxHeight),
        child: Stack(alignment: Alignment.center, children: [
          GestureDetector(
            onTap: widget.tapZoom ? () { if (ok) openFigure(context, widget.url); } : null,
            child: img,
          ),
          Positioned(
            right: 0,
            top: 0,
            child: GestureDetector(
              onTap: () => openFigure(context, widget.url),
              child: Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(color: const Color(0xCCFFFFFF), borderRadius: BorderRadius.circular(8), border: Border.all(color: const Color(0xFFE2E8F0))),
                child: const Icon(Icons.zoom_out_map, size: 16, color: Color(0xFF475569)),
              ),
            ),
          ),
        ]),
      ),
    );
  }
}
