#!/bin/bash

# سكريبت إعداد المهام التلقائية (Cron Jobs) لمشروع POP Materials

PROJECT_DIR="/opt/pop-materials"
CRON_FILE="/tmp/pop-materials-cron"

echo "⏰ إعداد المهام التلقائية لمشروع POP Materials..."

# إنشاء ملف cron مؤقت
cat > $CRON_FILE << EOF
# مهام تلقائية لمشروع POP Materials
# تم إنشاؤها تلقائياً في $(date)

# مراقبة التطبيق كل 5 دقائق
*/5 * * * * cd $PROJECT_DIR && ./monitor.sh monitor >> /var/log/pop-materials-cron.log 2>&1

# نسخة احتياطية يومية في الساعة 2:00 صباحاً
0 2 * * * cd $PROJECT_DIR && cp database.db /opt/backups/pop-materials/database_\$(date +\%Y\%m\%d_\%H\%M\%S).db

# نسخة احتياطية أسبوعية للصور (كل أحد في الساعة 3:00 صباحاً)
0 3 * * 0 cd $PROJECT_DIR && tar -czf /opt/backups/pop-materials/uploads_\$(date +\%Y\%m\%d_\%H\%M\%S).tar.gz static/uploads/

# تنظيف تلقائي أسبوعي (كل اثنين في الساعة 4:00 صباحاً)
0 4 * * 1 cd $PROJECT_DIR && ./monitor.sh cleanup >> /var/log/pop-materials-cron.log 2>&1

# حذف النسخ الاحتياطية القديمة (أكثر من 30 يوم) كل أسبوع
0 5 * * 1 find /opt/backups/pop-materials -name "*.db" -mtime +30 -delete
0 5 * * 1 find /opt/backups/pop-materials -name "*.tar.gz" -mtime +30 -delete

# تجديد شهادة SSL تلقائياً (كل يوم في الساعة 12:00 ظهراً)
0 12 * * * /usr/bin/certbot renew --quiet --no-self-upgrade

# إعادة تشغيل Nginx بعد تجديد الشهادة (إذا لزم الأمر)
5 12 * * * /bin/systemctl reload nginx

# مراقبة شاملة أسبوعية (كل جمعة في الساعة 1:00 صباحاً)
0 1 * * 5 cd $PROJECT_DIR && ./monitor.sh full >> /var/log/pop-materials-weekly.log 2>&1

# تنظيف لوجز Docker القديمة (كل شهر)
0 6 1 * * docker system prune -f --volumes >> /var/log/docker-cleanup.log 2>&1

EOF

# تثبيت cron jobs
echo "📝 تثبيت المهام التلقائية..."
crontab $CRON_FILE

# حذف الملف المؤقت
rm $CRON_FILE

# إنشاء مجلد النسخ الاحتياطية
mkdir -p /opt/backups/pop-materials

# تعيين الصلاحيات
chmod +x $PROJECT_DIR/monitor.sh
chmod +x $PROJECT_DIR/deploy-production.sh

echo "✅ تم إعداد المهام التلقائية بنجاح!"
echo ""
echo "📋 المهام المثبتة:"
echo "  - مراقبة التطبيق: كل 5 دقائق"
echo "  - نسخة احتياطية يومية: 2:00 ص"
echo "  - نسخة احتياطية أسبوعية للصور: الأحد 3:00 ص"
echo "  - تنظيف تلقائي: الاثنين 4:00 ص"
echo "  - حذف النسخ القديمة: الاثنين 5:00 ص"
echo "  - تجديد SSL: يومياً 12:00 ظ"
echo "  - مراقبة شاملة: الجمعة 1:00 ص"
echo "  - تنظيف Docker: شهرياً"
echo ""
echo "📁 مجلد النسخ الاحتياطية: /opt/backups/pop-materials"
echo ""
echo "🔍 لعرض المهام الحالية: crontab -l"
echo "📝 لتعديل المهام: crontab -e"