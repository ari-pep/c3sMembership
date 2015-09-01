# -*- coding: utf-8 -*-

# german template for *normal* members; see placeholder list below!
dues_invoice_mailbody_normal_de = u'''

Hallo {0} {1},

am 16.07.2015 hat die außerordentliche Mitgliederversammlung der C3S SCE eine
vorläufige Beitragsordnung erlassen, weil uns sonst die finanzielle Basis
fehlt, um unser gemeinsames Vorhaben fortsetzen zu können:

  https://archive.c3s.cc/aktuell/legal/C3S_SCE_membership_dues_de.pdf

Der Mitgliedsbeitrag für ordentliche Mitglieder für 2015 beträgt
demnach 50,- Euro für das ganze Jahr 2015.

Dein Mitgliedsbeitrag {5} beträgt demnach {3} Euro.

Bitte überweise {3} Euro auf folgendes Konto der C3S SCE:

  Verwendungszweck: {2}
  IBAN: DE79 8309 4495 0003 2643 78
  BIC: GENODEF1ETK
  Bank: Ethikbank

Bei der Überweisung des Mitgliedsbeitrags bitte den folgenden Verwendungszweck
angeben, damit die Zahlung zweifelsfrei Dir zugeordnet werden kann:
{2}

Die Rechnung findest Du unter folgendem Link:

  {4}

Vielen Dank für Deinen Support!

Dein C3S Team

'''
# format strings:
# {0}: first name
# {1}: last name
# {2}: referral code: C3S-dues2015-ABCDEFGH
# {3}: dues, maybe partial, depending on entry date
# {4}: link to invoice PDF
# {5}: dues start quarter, e.g. "ab Quartal 2"

# english template for *normal* members; see placeholder list below!
dues_invoice_mailbody_normal_en = u'''[english version below]

Hello {0} {1},

On July 16th, 2015, the extraordinary general assembly of the C3S has issued
temporary membership contribution rules, in order to secure the financial
basis for the continuation of our common project:

  https://archive.c3s.cc/aktuell/legal/C3S_SCE_membership_dues_de.pdf

For 2015, the membership dues for active members will therefore be 50,- Euro.

Please transfer {3} Euro to the following account of the C3S SCE:

  Purpose: {2}
  IBAN: DE79 8309 4495 0003 2643 78
  BIC: GENODEF1ETK
  Bank: Ethikbank

In order to enable the proper allocation of your membership dues, please
add the following purpose: {2}

You will find the invoice here:

  {4}

Many thanks for your support!

Your C3S team

'''
# format strings:
# {0}: first name
# {1}: last name
# {2}: referral code: C3S-dues2015-ABCDEFGH
# {3}: dues, maybe partial, depending on entry date
# {4}: link to invoice PDF


# german template for *investing* members; see placeholder list below!
dues_invoice_mailbody_investing_de = u'''

Hallo {0} {1},

am 16.07.2015 hat die außerordentliche Mitgliederversammlung der C3S SCE eine
vorläufige Beitragsordnung erlassen, weil uns sonst die finanzielle Basis
fehlt, um unser gemeinsames Vorhaben fortsetzen zu können:

  https://archive.c3s.cc/aktuell/legal/C3S_SCE_membership_dues_de.pdf

Der Mitgliedsbeitrag für ordentliche Mitglieder für 2015 beträgt
demnach 50,- Euro.

Da Du investierendes Mitglied bist, bist Du vom Mitgliedsbeitrag
befreit. Du würdest der C3S aber sehr helfen, wenn Du dennoch
freiwillig einen Beitrag leisten würdest.

Wenn Du uns unterstützen möchtest, überweise Deine freiwillige
Zuwendung auf folgendes Konto:

  Verwendungszweck: {2}
  IBAN: DE79 8309 4495 0003 2643 78
  BIC: GENODEF1ETK
  Bank: Ethikbank


Vielen Dank für Deinen Support!

Dein C3S Team

'''
# format strings:
# {0}: first name
# {1}: last name
# {2}: referral code: C3S-dues2015-ABCDEFGH


# english template for *investing* members; see placeholder list below!
dues_invoice_mailbody_investing_en = u'''

Hello {0} {1},

On July 16th, 2015, the extraordinary general assembly of the C3S has issued
temporary membership contribution rules, in order to secure the financial basis
for the continuation of our common project:

  https://archive.c3s.cc/aktuell/legal/C3S_SCE_membership_dues_de.pdf

For 2015, the membership dues for active members will therefore be 50,- Euro.

Since you are an investing member, you are exempt from this payment.
However, your voluntary contribution would be highly appreciated as a
tremendous help for the C3S.

If you want to support us, please transfer your voluntary contribution to the
following account:

  Purpose:
  IBAN: DE79 8309 4495 0003 2643 78
  BIC: GENODEF1ETK
  Bank: Ethikbank

Many thanks for your support!

Your C3S team

'''
# format strings:
# {0}: first name
# {1}: last name
# {2}: referral code: C3S-dues2015-ABCDEFGH


# additional german snippet for *investing* members that are *legal entities*
dues_legalentities_de = u"""
Für juristische Personen wird empfohlen,
über den Grundbetrag hinaus einen Förderbeitrag
in folgender Höhe zu entrichten:

a) bis zu einem Jahresumsatz i. H. v. 100.000 Euro
   pro Jahr 100 Euro
b) bis zu einem Jahresumsatz i. H. v. 200.000 Euro
   pro Jahr 200 Euro
c) bei höherem Jahresumsatz ist die Höhe entsprechend anzupassen.

"""

# additional english snippet for *investing* members that are *legal entities*
dues_legalentities_en = u"""
For legal entities there is a recommendation to exceed the basic fee
by adding a supportive contribution of the following amount:

a) up to a yearly turnover of 100.000 Euro: 100 Euro per year
b) up to a yearly turnover of 200.000 Euro: 200 Euro per year
c) with higher turnover: raise fee accordingly.

"""


# # template for transferral receipt email
# dues_receipt_mail_de = u"""
# [english version below]

# Hallo {0} {1},

# wir haben deinen Mitgliedsbeitrag erhalten. Danke!

# Dein C3S Team

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Hello {0} {1},

# we received transfer of your membership dues. Thanks!


# Your C3S Team

# """
# # # format strings:
# # # 0: first name
# # # 1: last name
# # # 2: receipt link / URL


dues_update_reduction_de = u'''

Hallo {0} {1},

Du hast eine Reduzierung Deines Mitgliedsbeitrages beantragt.

Wir geben Deinem Antrag statt und reduzieren Deinen Beitrag daher auf € {2}.

Bitte überweise die genannte Summe auf folgendes Konto der C3S SCE:

  Verwendungszweck: {3}
  IBAN: DE79 8309 4495 0003 2643 78
  BIC: GENODEF1ETK
  Bank: Ethikbank

Gebe bei der Überweisung des Mitgliedsbeitrags bitte unbedingt den
oben genannten Verwendungszweck an, damit die Zahlung zweifelsfrei Dir
zugeordnet werden kann.

Hier ist die neue Rechnung als PDF:

  {4}

Die Storno-Rechnung zu Deiner ersten Beitragsrechnung findest Du hier:

  {5}

Vielen Dank für Deinen Support!
Dein C3S Team
'''


dues_update_reduction_en = u'''
Hello {0} {1},

You have applied for a reduction of your membership contributions.

We therefore reduce your dues to € {2}.

Please transfer the above-mentioned amount to the following account
of the C3S SCE:

  Purpose: {3}
  IBAN: DE79 8309 4495 0003 2643 78
  BIC: GENODEF1ETK
  Bank: Ethikbank

Please state the purpose on your transfer in order to enable the
proper allocation of your payment.

Here is the new invoice as a PDF document:

  {4}

You will find the reverse invoice of your first membership dues invoice here:

  {5}

Many thanks for your support!
Your C3S team
'''

dues_exemption_de = u"""
Hallo {0} {1},

Du hast eine Befreiung von der Zahlung des Mitgliedsbeitrages beantragt.

Wir geben Deinem Antrag statt und erlassen Dir die Beitragszahlung.

Die Storno-Rechnung zu deiner Beitragsrechnung findest du hier:

  {2}

Beste Grüße
Dein C3S Team
"""

dues_exemption_en = u"""

Hello {0} {1},

You have applied for exemption from your membership contributions.

We therefore exempt you from the payment of your dues.

You will find the reverse invoice of your membership dues invoice here:

  {2}

With best wishes
Your C3S team
"""
