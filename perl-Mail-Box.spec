#
# Conditional build:
%bcond_with	tests	# perform "make test"

%include	/usr/lib/rpm/macros.perl
%define	pdir	Mail
%define	pnam	Box
Summary:	Mail::Box - manage a mailbox, a folder with messages
Summary(pl):	Mail::Box - zarz±dzanie skrzynk±, folderem z wiadomo¶ciami
Name:		perl-Mail-Box
Version:	2.054
Release:	1
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	2805fa4567b577ff2e3f6ea76f9edd7f
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(Encode) >= 1.86
BuildRequires:	perl-Object-Realize-Later >= 0.12
BuildRequires:	perl(Scalar::Util) >= 1.07
BuildRequires:	perl-HTML-Format
BuildRequires:	perl-MIME-Types >= 1.004
BuildRequires:	perl-Mail-SpamAssassin
BuildRequires:	perl-Test-Simple >= 0.47
BuildRequires:	perl-Text-Autoformat
# not in PLD yet
#BuildRequires:	perl-Mail-Transport-Dbx >= 0.04
#BuildRequires:	perl-User-Identity
%endif
# not found by perl.req
Requires:	perl-Object-Realize-Later >= 0.12
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_noautoreq	'perl(Mail::SpamAssassin)' 'perl(Text::Autoformat)' 'perl(HTML::FormatText)' 'perl(Mail::Transport::Dbx).*'

%description
The Mail::Box folder is a modern mail-folder manager -- at least at
the moment of this writing ;)  It is written to replace Mail::Folder,
although it interface is different.

%description -l pl
Folder Mail::Box to wspó³czesny zarz±dca folderów pocztowych -
przynajmniej w chwili pisania ;). Jest pisany, aby zast±piæ
Mail::Folder, aczkolwiek interfejs jest inny.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%{__perl} -pi -e 's/^use 5.007003;$/use 5.007_003;/' Mail/Message/Field/Attribute.pm

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	< /dev/null
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name '*.pod' -exec rm -f '{}' \;

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -r examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL README* TODO*
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}
%{perl_vendorlib}/Mail/*
%{_mandir}/man3/*
