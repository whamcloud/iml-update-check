BUILDROOT:=$(shell [ -d "/build" ] && echo "/build" || echo ".")
TMPDIR:=$(shell mktemp -d)

srpm:
	mkdir -p ${TMPDIR}/_topdir/{SOURCES/iml-update-check,SPECS}
	rm -rf ${BUILDROOT}/_topdir
	cp iml-update-check.{service,timer} \
		iml-update-handler.{service,socket} \
		iml-update-check.py \
		handler.js \
		README.md \
		${TMPDIR}/_topdir/SOURCES/iml-update-check/
	tar -czvf ${TMPDIR}/_topdir/SOURCES/iml-update-check.tar.gz -C ${TMPDIR}/_topdir/SOURCES/iml-update-check .
	cp iml-update-check.spec ${TMPDIR}/_topdir/SPECS/
	rpmbuild -bs -D "_topdir ${TMPDIR}/_topdir" ${TMPDIR}/_topdir/SPECS/iml-update-check.spec
	cp -rf ${TMPDIR}/_topdir ${BUILDROOT}/
	cp -f _topdir/SRPMS/*.rpm $(outdir)

