// TSSC-DISCLAIMER-V1 (2026-11-18): Google Play "Misleading Claims" fix.
// The app is not a government app; every exam / government fact links to its official source.
// Shown on the sign-in screen (GovDisclaimer) and in Me tab -> "Disclaimer & official sources".
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../ui/soft.dart';

const disclaimerText =
    'TrickySSC is a private exam-practice app. It is not affiliated with, endorsed by or representing the Staff Selection Commission (SSC), '
    'the Railway Recruitment Boards (RRB), Indian Railways or any government body. For official notices, dates, syllabus, '
    'admit cards and results, always check the official websites below.';

const officialSources = [
  ('Staff Selection Commission (SSC)', 'Notices, exam calendar, syllabus, admit cards, answer keys and results', 'https://ssc.gov.in'),
  ('RRB — official application portal', 'RRB NTPC, Station Master, Group D: apply and check notices', 'https://www.rrbapply.gov.in'),
  ('RRB Chandigarh (official RRB website)', 'RRB CEN notices and results', 'https://www.rrbcdg.gov.in'),
  ('Indian Railways', 'Ministry of Railways, Government of India', 'https://indianrailways.gov.in'),
  ('Press Information Bureau (PIB)', 'Source for government news used in current affairs', 'https://pib.gov.in'),
  ('Union Budget & Economic Survey', 'Ministry of Finance, Government of India', 'https://www.indiabudget.gov.in'),
  ('National Portal of India', 'Government schemes and general information', 'https://www.india.gov.in'),
];

Future<void> openLink(BuildContext context, String url) async {
  final ok = await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication).catchError((_) => false);
  if (!ok && context.mounted) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Open $url in your browser')));
  }
}

/// Short disclaimer box with a link to the full page. Used on the sign-in screen.
class GovDisclaimer extends StatelessWidget {
  const GovDisclaimer({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(12, 10, 12, 6),
      decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(14), border: Border.all(color: const Color(0xFFE2E8F0))),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text(
          'Not a government app. TrickySSC is not affiliated with SSC, RRB or any government body. Official information: ssc.gov.in and rrbapply.gov.in.',
          style: TextStyle(fontSize: 12.5, color: Color(0xFF475569), height: 1.35, fontWeight: FontWeight.w600),
        ),
        Align(
          alignment: Alignment.centerLeft,
          child: TextButton(
            style: TextButton.styleFrom(padding: EdgeInsets.zero, minimumSize: const Size(0, 34)),
            onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const AboutPage())),
            child: const Text('Disclaimer & official sources', style: TextStyle(fontWeight: FontWeight.w800)),
          ),
        ),
      ]),
    );
  }
}

class AboutPage extends StatelessWidget {
  final Color color;
  const AboutPage({super.key, this.color = const Color(0xFFFF6B00)});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: softBg,
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(title: const Text('Disclaimer & official sources'), backgroundColor: Colors.transparent, elevation: 0),
        body: ListView(
          padding: EdgeInsets.fromLTRB(16, 8, 16, 24 + MediaQuery.of(context).padding.bottom),
          children: [
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(color: const Color(0xFFFFF7ED), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFFED7AA))),
              child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('⚠️ Disclaimer', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900, color: Color(0xFF7C2D12))),
                SizedBox(height: 6),
                Text(disclaimerText, style: TextStyle(fontSize: 14, height: 1.45, color: Color(0xFF7C2D12), fontWeight: FontWeight.w600)),
                SizedBox(height: 8),
                Text(
                  'Previous year questions are reproduced from papers released publicly by the exam bodies for practice. Mock tests, solutions and notes are made by TrickySSC.',
                  style: TextStyle(fontSize: 13, height: 1.4, color: Color(0xFF9A3412)),
                ),
              ]),
            ),
            const SizedBox(height: 16),
            const Text('Official sources', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900, color: softInk)),
            const SizedBox(height: 8),
            for (final s in officialSources)
              Card(
                elevation: 0,
                color: Colors.white,
                margin: const EdgeInsets.only(bottom: 8),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14), side: const BorderSide(color: Color(0xFFE2E8F0))),
                child: ListTile(
                  onTap: () => openLink(context, s.$3),
                  leading: const Icon(Icons.account_balance_rounded, color: Color(0xFF1D4ED8)),
                  title: Text(s.$1, style: const TextStyle(fontWeight: FontWeight.w800)),
                  subtitle: Text('${s.$2}\n${s.$3}', style: const TextStyle(height: 1.35)),
                  isThreeLine: true,
                  trailing: const Icon(Icons.open_in_new_rounded, size: 20),
                ),
              ),
            const SizedBox(height: 10),
            const Text('Contact: contact@trickyssc.com · trickyssc.com', style: TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
          ],
        ),
      ),
    );
  }
}
