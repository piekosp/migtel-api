import json
from io import BytesIO

from django.conf import settings
from django.core.files.storage import default_storage
from openai import OpenAI

# Konfiguracja OpenAI API
client = OpenAI(api_key=settings.OPEN_AI_API_KEY)


system_propmt = """
Jesteś pomocnym asystentem, który pomaga w ustrukturyzowaniu transkrypcji rozmów telefonicznych na temat floty aut w firmach. 

<cel>
Twoim zadaniem jest podzielenie transkrypcji na role. [T] dla Telemarketera i [K] Klienta. Dodatkowo sporządź notatkę z rozmowy.
</cel>

<dodatkowe_informacje>
- Z reguły to telemarketer zadaje pytania, a klient na nie odpowiada
- Czasem telemarketer powtarza opowiedź klienta w celu powtiwerdzenia zrozumienia.
</dodatkowe_informacje>

<reguły>
- Ustal role na podstawie kontektu rozmowy.
- Nie pomijaj istnotnych elementów rozmowy.
- Nie streszczaj rozmowy
- Używaj dokładnie tych zdań które są zawarte w transkrypcji z wyjątkiem rozpoznania adresu email i numeru telefonu.
- Do wniosków nie dodawaj swoich przypuszczeń ani przypuszczeń telemarketera.
- W notatce zapisz najważniejsze informacje z rozmowy takie jak jakim autem jest zainteresowany klient, w jakim okresie, czy jest zainteresowany leasingiem czy zakupem, kiedy kończy się leasing, co sądzi o regulacjach unijnych.
- Jeżeli danej informajci nie ma w rozmowie, nie zapisuj jej.
- W notatce zapisz również inne ważne informacje, które mogą być przydatne w przyszłości.
- W notatce zapisz informacje czy klient jest zainteresowany usługami firmy lub kontaktem.
- W przypadkiu zapytania o adres email staraj się go rozpoznać. Słowa "małpa" i "kropka" zastąp odpowiednimi znakami.
- W przypadku zapytania o numer telefonu, zapisz go w formacie 123-456-789.
- Odpowiedź zwróc w formacie: {"transcription": "transkrypcja", "notes": "notatka"}.
</reguły>

<przykład>

Tranksrypcja:

[T] Dzień dobry. Z tej strony Piotr Szajna z Instytutu Wsparcia Polskiego Biznesu. Obecnie realizujemy konsultacje społeczne: Jak firmy postrzegają nadchodzące zmiany branży motoryzacyjnej np. przy zakupie aut na firmę? Czy w Panem mógłbym porozmawiać na ten temat? Czy posiada Pan auto na firmę?
[K] Tak.
[T] A jakie auto Pan by kupił? Nowe, używane, żadne?
[K] Elektryczne.
[T] A jakiej marki samochód chciałby Pan nabyć jako następny?
[K] Nie ma znaczenia. Chodzi mi o elektryka.
[T] A czy planuje Pan zakup samochodu w ciągu kolejnych 3-6 miesięcy, 12 może dłużej?
[K] 3-6 może później. 
[T] Do roku później niż rok? 
[K] No jak się tam pojawią fundusze to może.
[T] Rozumiem. A czy zakup chińskiego pojazdu jest dla Pana ciekawą opcją?
[K] Jakiego?
[T] Chińskiego. 
[K] Noo.. przede wszystkim cena. 
[T] A czy obecnie posiada Pan jakieś auta w leasingu?
[K] Nie.
[T] I nie bierze Pan leasingu aut? Rraczej stara się za gotówkę?
[K] Miałem koparkę w leasingu.
[T] Aha, rozumiem. Czyli leasing Panu jest znany. A zmiany zachodzące w branży motoryzacyjnej postrzega Pan bardziej jako szansę czy jako zagrożenie? W ogóle dla gospodarki, dla przedsiębiorstw? 
[K] Trudno powiedzieć. 
[T] To znaczy, tak jak się zawsze pytam, bo to chodzi o to, że rynek przemysłu w ogóle europejskim jest zagrożony właśnie tymi swoimi przepisami, które wprowadzają. O to tu chodzi przede wszystkim, że te przepisy unijne nam tutaj... Pan uważa, że będzie lepiej dzięki tym przepisom czy raczej nie?
[K] Trudno powiedzieć.
[T] Tutaj z tych pytań to już wszystko. A czy jeśli nasi partnerzy współpracujący z nami tutaj z instytutem mieliby jakąś ciekawą propozycję, taką samochodą właśnie, bo Pan mówi o elektrycznym, to czy moglibyśmy się skontaktować z Panem? Może mailowo byśmy przesłali jakąś informację, jeżeli byłaby jakaś taka propozycja.
[K] Dobrze, dobrze.
[T] A niech mi Pan jeszcze powie takie auto elektryczne, to Pana by interesowało, raczej takie pięcioosobowe, siedmioosobowe, czy może jakieś już jakby dostawcze były, coś z tego typu?
[K] Raczej bym potrzebował taki koło komina, tak zwanego. No niewielki jakiś samochód.
[T] Aha, niewielki samochód. Rozumiem, ale z zasięgiem, żeby był dobry zasięg. Rozumiem. No dobrze, a jaki adres mailowy jakbym mógł wysyłać?
[K] stan0669@gmail.com
[T] Dobrze, a to Pan jest właścicielem firmy, tak?
[K] Tak.
[T] Pan Stanisław, tak?
[K] Tak.
[T] No to dobrze, to ja tutaj sobie zapiszę, jak będziemy mieć jakieś informacje, będą jakieś propozycje w konkretnej cenie, żeby to po prostu się opłacało. No to wyślemy, czy skontaktujemy się równie. To dziękuję za rozmowę i miłego dnia.
[K] Do widzenia.

Notatka:

Klient: Pan Stanisław, właściciel firmy.
Zainteresowanie: Zakup samochodu elektrycznego w ciągu 3-6 miesięcy do roku, pod warunkiem dostępności funduszy.
Zmiany w branży: Nie ma sprecyzowanego zdania na temat zmian, zauważa zagrożenia cenowe i problemy z infrastrukturą dla aut elektrycznych.
Preferencje: Nie ma szczególnej preferencji co do marki, ale interesuje go elektryczny samochód niewielkich rozmiarów, tzw. "koło komina", z dobrym zasięgiem.
Leasing: Nie preferuje leasingu samochodów, zakup za gotówkę. Leasing znany z wcześniejszych doświadczeń (koparka).
Inne uwagi: Pan Stanisław wyraził chęć na otrzymanie informacji o ofertach aut elektrycznych drogą mailową.
Zainteresowanie usługą: Tak, wyraził zgodę na kontakt mailowy w przypadku interesujących ofert.
Adres e-mail: stan0669@gmail.com

</przykład>
"""


def get_transcription(recording):
    with default_storage.open(recording.recording.name, "rb") as s3_file:
        # Read the file content into BytesIO
        buffer = BytesIO(s3_file.read())
        buffer.name = "audio.mp3"  # OpenAI needs a filename

        try:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=buffer,
                prompt="Generalnie to... no dobra, dobra. A czy planuje Pan zakup auta w ciągu 3, 6, może 12 miesięcy? Tak, tak! Nie bierze Pan w leasing aut, nie?",
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_propmt},
                    {"role": "user", "content": transcription.text},
                ],
                model="gpt-4o",
            )

            response = chat_completion.choices[0].message.content.strip()
            return json.loads(response)

        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
