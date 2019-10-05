#
# Conditional build:
%bcond_with	tests	# perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Mail
%define		pnam	Box
Summary:	Mail::Box - manage a mailbox, a folder with messages
Summary(pl.UTF-8):	Mail::Box - zarządzanie skrzynką, folderem z wiadomościami
Name:		perl-Mail-Box
Version:	3.006
Release:	1
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Mail/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	e9d277d86e3f557c9feb69781cd9eee5
URL:		http://search.cpan.org/dist/Mail-Box/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Date::Parse)
BuildRequires:	perl-Devel-GlobalDestruction >= 0.09a3
BuildRequires:	perl(Encode) >= 1.86
BuildRequires:	perl-File-Remove >= 0.2
BuildRequires:	perl(IO::Scalar)
BuildRequires:	perl-Object-Realize-Later >= 0.19
BuildRequires:	perl(Scalar::Util) >= 1.07
BuildRequires:	perl-HTML-Format
BuildRequires:	perl-MIME-Types >= 1.004
BuildRequires:	perl-Mail-SpamAssassin
BuildRequires:	perl-Test-Simple >= 0.47
BuildRequires:	perl-Text-Autoformat
BuildRequires:	perl-User-Identity
%endif
# not found by perl.req
Requires:	perl-Object-Realize-Later >= 0.19
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_noautoreq	'perl(Mail::SpamAssassin)' 'perl(Text::Autoformat)' 'perl(HTML::FormatText)' 'perl(Mail::Transport::Dbx).*'

%description
The Mail::Box folder is a modern mail-folder manager -- at least at
the moment of this writing ;)  It is written to replace Mail::Folder,
although it interface is different.

%description -l pl.UTF-8
Folder Mail::Box to współczesny zarządca folderów pocztowych -
przynajmniej w chwili pisania ;). Jest pisany, aby zastąpić
Mail::Folder, aczkolwiek interfejs jest inny.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

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
%doc ChangeLog README*
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}
%{perl_vendorlib}/Mail/*
%{_mandir}/man3/*
