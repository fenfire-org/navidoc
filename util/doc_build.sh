#! /bin/bash

# Doc_build.sh
#
# simple uml and javadoc robot for Gzz documentation.
# mudyc, 2002-08-22T16:53:06
#
# port to fenfire at ma huhti   7 08:33:42 EEST 2003

#export CLASSPATH=$CLASSPATH:${JAVA_HOME}/lib/tools.jar
#export PATH=${PATH}:~/src/bin/

export JAVAHOME=/usr/j2sdk1.4.1_01/
export CLASSPATH=/usr/j2sdk1.4.1_01/jre/lib/rt.jar
export PATH=/usr/j2sdk1.4.0/bin/:/usr/local/bin:/usr/bin:/bin:


# directory
DIR=/home/mudyc/doc_build_script/src/

# files
ERRORS=$DIR/Doc_build.log

#opts
MAKE_OPT='-s '
MAKE="make $MAKE_OPT"

# destiny
DEST="mudyc@himalia.it.jyu.fi"
DEST_DIR="/var/www/ffdoc/"

SSH_OPTS="-2 -q -i /home/mudyc/.ssh/id_dsa_himalia_bot"


# Copy old Log - so we can diff..
# ===============================
cd $DIR
cp $ERRORS $ERRORS.old


# leave a mark in errors login
# ============================
cd $DIR
echo "***************************************" > $ERRORS
echo "** Doc_build.log **********************" >> $ERRORS
echo "***************************************" >> $ERRORS
date >> $ERRORS
echo "***************************************" >> $ERRORS


# Cleaning to make room for new docs
# ==================================
 #cd $GZ_DIR
 #make $MAKE_OPT clean 2>>$ERRORS
# although gzz/doc/javadoc doesn't clean I think

echo "update CVS"

# update from cvs
# ===============
cd $DIR
for x in `ls -1|grep -v Doc`; 
  do cd $DIR/$x &&  cvs up -dP 2>>$ERRORS; 
done;

echo "Making"

# set special settings for navidoc
mkdir -p $DIR/ffdoc
mkdir -p $DIR/ffdoc/diagrams
cp $DIR/navidoc/config.himalia $DIR/navidoc/config.py
cp $DIR/navidoc/gzz.css $DIR/ffdoc/gzz.css
cp $DIR/navidoc/docutils.himalia $DIR/navidoc/docutils.conf
cp $DIR/navidoc/navidoc/mp/*.tfm $DIR/ffdoc/diagrams

# make uml, javadoc, pegs etc...
# ========================
cd $DIR
for x in `ls -1|grep -v Doc|grep -v depend|grep -v ffdoc`;
  do cd $DIR/$x  && \
      pwd && \
      $MAKE docs 1>/dev/null 2>>$ERRORS #&& \
      #$MAKE pegs 1>/dev/null 2>>$ERRORS; 
done;
echo '...done'

#cd $GZ_DIR
#make $MAKE_OPT doc 1>/dev/null 2>> $ERRORS
#make rst RST="doc/pp/coords.rst" 1>/dev/null 2>> $ERRORS


# Make diff of the log of yesterday
# =================================
diff -u $ERRORS.old $ERRORS > $ERRORS.diff


# Compine diff and real errors to one file
# ========================================
cat $ERRORS.diff > $ERRORS.real
echo "     *       *     " >> $ERRORS.real
echo "*** * * *** * * ***" >> $ERRORS.real
echo "     *       *     " >> $ERRORS.real
cat $ERRORS >> $ERRORS.real


# remove old documentation from remote
# ====================================
ssh $SSH_OPTS $DEST rm -r $DEST_DIR/*


# secure-copy new docs to http server
# ===================================
echo "Copy"
cd $DIR
for x in `ls -1|grep -v Doc|grep -v fenfire|grep -v depend|grep -v ffdoc`;
  do ssh $SSH_OPTS $DEST mkdir $DEST_DIR/$x && \
      scp $SSH_OPTS -r $DIR/$x/doc/* $DEST:$DEST_DIR/$x/
done;
# fenfire is special ;)
ssh $SSH_OPTS $DEST mkdir $DEST_DIR/fenfire && \
    scp $SSH_OPTS -r $DIR/fenfire/docs/* $DEST:$DEST_DIR/fenfire/

# diagrams
ssh $SSH_OPTS $DEST mkdir $DEST_DIR/diagrams && \
    scp $SSH_OPTS -r $DIR/ffdoc/diagrams/* $DEST:$DEST_DIR/diagrams/
scp $SSH_OPTS -r $DIR/ffdoc/gzz.css $DEST:$DEST_DIR/gzz.css
echo "..done"

echo "Copy log"
cd $DIR
scp $SSH_OPTS $ERRORS.real $DEST:$DEST_DIR/Doc_build.log
echo "..done"


