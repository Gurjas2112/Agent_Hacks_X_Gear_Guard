# GearGuard - Odoo 17 Maintenance Module
# Dockerfile for containerized deployment

FROM odoo:17.0

# Maintainer information
LABEL maintainer="GearGuard Team <gearguard@example.com>"
LABEL description="GearGuard - The Ultimate Maintenance Tracker for Odoo 17"
LABEL version="17.0.1.0.0"

# Switch to root for installations
USER root

# Install additional Python dependencies (if needed)
RUN pip3 install --no-cache-dir \
    python-dateutil \
    pytz

# Create addons directory structure
RUN mkdir -p /mnt/extra-addons/gearguard

# Copy the GearGuard module
COPY ./gearguard /mnt/extra-addons/gearguard

# Set proper permissions
RUN chown -R odoo:odoo /mnt/extra-addons/gearguard

# Switch back to odoo user
USER odoo

# Expose Odoo ports
EXPOSE 8069 8071 8072

# Default command
CMD ["odoo"]
