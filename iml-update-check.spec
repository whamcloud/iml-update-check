Summary: IML Software Update Checker
Name: iml-update-check
Version: 1.0.2
# Release Start
Release: 1%{?dist}
# Release End

License: MIT
Group: Development/Libraries
URL: https://github.com/whamcloud/iml-update-check
Source0: iml-update-check.tar.gz

%{?systemd_requires}
BuildRequires: systemd
BuildArch: noarch

%package -n iml-update-handler
Summary: IML Handler for Update Checker
Requires: nodejs
%{?systemd_requires}
BuildRequires: systemd
BuildArch: noarch

%description
Periodically check for package updates

%description -n iml-update-handler
Respond to update check information:
- Raise Alert in IML if true
- Lower Alert in IML if false

%prep
%setup -qc

%build
# no build

%install
rm -rf $RPM_BUILD_ROOT
install -p -D -m 0755 iml-update-check.py $RPM_BUILD_ROOT/%{_bindir}/iml-update-check
install -p -D handler.js $RPM_BUILD_ROOT/%{_libexecdir}/iml-update-handler.js

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}/
cp iml-update-check.service $RPM_BUILD_ROOT/%{_unitdir}/
cp iml-update-check.timer $RPM_BUILD_ROOT/%{_unitdir}/
cp iml-update-handler.service $RPM_BUILD_ROOT/%{_unitdir}/
cp iml-update-handler.socket $RPM_BUILD_ROOT/%{_unitdir}/

mkdir -p %{buildroot}%{_presetdir}
cp 00-iml-update-check.preset %{buildroot}%{_presetdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post iml-update-check.timer iml-update-check.service

%preun
%systemd_preun iml-update-check.timer iml-update-check.service

%postun
%systemd_postun_with_restart iml-update-check.timer iml-update-check.service

%post -n iml-update-handler
%systemd_post iml-update-handler.socket iml-update-handler.service

%preun -n iml-update-handler
%systemd_preun iml-update-handler.socket iml-update-handler.service

%postun -n iml-update-handler
%systemd_postun_with_restart iml-update-handler.socket iml-update-handler.service


%files
%defattr(-,root,root,-)
%doc README.md
%{_bindir}/iml-update-check
%{_unitdir}/iml-update-check.*
%{_presetdir}/00-iml-update-check.preset

%files -n iml-update-handler
%defattr(-,root,root,-)
%{_libexecdir}/iml-update-handler.js
%{_unitdir}/iml-update-handler.*

%changelog
* Mon May 13 2019 Joe Grund <jgrund@whamcloud.com> - 1.0.2-1
- Fix requirement on socket instead of service

* Tue Apr 23 2019 Joe Grund <jgrund@whamcloud.com> - 1.0.1-1
- Refactor packaging.
- Use yum to scan.
- Restart service after 5 minutes on failure.

* Mon Jul  2 2018 Nathaniel Clark <nclark@whamcloud.com> - 0.1-1
- Initial build.

