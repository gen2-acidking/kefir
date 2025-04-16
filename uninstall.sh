#!/bin/bash

##################################################################
# Kefir uninstall Script
# author: gen2acidking 
##################################################################

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' 
INSTALL_DIR="$HOME/.kefir"

echo -e "${YELLOW}Uninstalling Kefir...${NC}"

"$INSTALL_DIR/kefir" --stop 2>/dev/null
if [ -L "/usr/local/bin/kefir" ]; then
    echo -e "${YELLOW}Removing symlink...${NC}"
    sudo rm -f /usr/local/bin/kefir
fi

if grep -q "alias kefir=" "$HOME/.bashrc"; then
    echo -e "${YELLOW}Removing alias from .bashrc...${NC}"
    sed -i '/alias kefir=/d' "$HOME/.bashrc"
fi

if [ -f "$HOME/.zshrc" ] && grep -q "alias kefir=" "$HOME/.zshrc"; then
    echo -e "${YELLOW}Removing alias from .zshrc...${NC}"
    sed -i '/alias kefir=/d' "$HOME/.zshrc"
fi

echo -e "${YELLOW}Removing installation directory...${NC}"
rm -rf "$INSTALL_DIR"

if [ -f "$HOME/.kefir.pid" ]; then
    rm -f "$HOME/.kefir.pid"
fi

echo -e "${GREEN}Kefir has been uninstalled successfully!${NC}"
echo -e "Please restart your terminal or run: ${YELLOW}source ~/.bashrc${NC} to apply changes."
